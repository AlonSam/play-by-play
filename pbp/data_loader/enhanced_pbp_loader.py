"""
will load pbp from each resource and convert to same pattern
"""

from collections import defaultdict

from pbp.resources.enhanced_pbp import Foul, StartOfPeriod


class EnhancedPbpLoader(object):
    """
    Base class for all EnhancedPbpLoaders.
    This class should not be instantiated directly.
    """

    def _add_extra_attrs_to_all_events(self):
        """
        adds fouls to give, player fouls, next event and previous event to each event
        """
        self.start_period_indices = []
        fouls_to_give = defaultdict(lambda: 4)
        player_game_fouls = defaultdict(int)
        for i, event in enumerate(self.items):
            event.game_id = int(self.game_id)
            if i == 0 and i == len(self.items) - 1:
                # Just 1 event in list
                event.previous_event = None
                event.next_event = None
            elif isinstance(event, StartOfPeriod) or i == 0:
                if i != 0:
                    event.previous_event = self.items[i - 1]
                else:
                    event.previous_event = None
                event.next_event = self.items[i + 1]
                self.start_period_indices.append(i)
                if event.period <= 4:
                    fouls_to_give = defaultdict(lambda: 4)
            elif i == len(self.items) - 1 or event.period != self.items[i + 1].period:
                event.previous_event = self.items[i - 1]
                event.next_event = None
            else:
                event.previous_event = self.items[i - 1]
                event.next_event = self.items[i + 1]
            if isinstance(event, Foul):
                t = str(event.team_id)
                p = str(event.player_id)
                if event.counts_towards_penalty and fouls_to_give[t] > 0:
                    fouls_to_give[t] -= 1
                if event.counts_as_personal_foul:
                    player_game_fouls[p] += 1
            event.fouls_to_give = fouls_to_give.copy()
            event.player_game_fouls = player_game_fouls.copy()
        self._set_period_starters()
        self._add_score_and_margin_to_all_events()
        self._add_offense_team_id_to_all_events()

    def combine_related_events(self):
        """
        Used only by Euroleague and ACB.
        Will get overwritten for FIBA and Segev.
        """
        for i, event in enumerate(self.items):
            if event.action_type == 'turnover':
                self.event_within_5_seconds(event, i, 'steal')
                if not hasattr(event, 'steal'):
                    # Check if steal appears before turnover
                    prev_event = self.items[i - 1]
                    if prev_event.action_type == 'steal' and event.team != prev_event.team:
                        event.steal = prev_event.player_id
                        self.items.remove(prev_event)
            elif 'pt' in event.action_type or event.action_type == 'freethrow':
                if event.made:
                    self.event_within_5_seconds(event, i, 'assist')
                    if not hasattr(event, 'assist'):
                        # Check if assist appears before shot
                        prev_events = self.get_previous_events_at_current_time(event, i)
                        for prv in prev_events:
                            if prv.action_type == 'assist' and event.team == prv.team:
                                event.assist = prv.player_id
                                self.items.remove(prv)

                elif 'pt' in event.action_type:
                    self.event_within_5_seconds(event, i, 'block')
            elif event.action_type == 'blocked':
                self.items.remove(event)
            elif event.action_type == 'foul':
                self.event_within_5_seconds(event, i, 'foul_on')
                if not hasattr(event, 'foul_on'):
                    # Check if foul_on appears before foul
                    prev_event = self.items[i - 1]
                    if prev_event.action_type == 'foul_on' and event.team != prev_event.team:
                        event.steal = prev_event.player_id
                        self.items.remove(prev_event)
            elif event.action_type == 'substitution':
                if event.sub_type == 'in':
                    self.event_within_5_seconds(event, i, 'out')
                    if not hasattr(event, 'sub_out_player_id'):
                        raise Exception('Substitution in has no related event')
                    event.sub_in_player_id = event.player_id
                else:
                    self.event_within_5_seconds(event, i, 'in')
                    if not hasattr(event, 'sub_in_player_id'):
                        raise Exception('Substitution out has no related event')
                    event.sub_out_player_id = event.player_id
                delattr(event, 'player')
                delattr(event, 'player_id')
                delattr(event, 'num')
                event.sub_type = ''

    def event_within_5_seconds(self, event, idx, action):
        while idx < len(self.items) - 1:
            next_event = self.items[idx + 1]
            if event.period == next_event.period and event.seconds_remaining - next_event.seconds_remaining <= 5:
                if next_event.action_type == action or next_event.sub_type == action:
                    team_actions = ['assist_player_id', 'in', 'out']
                    if (action in team_actions and event.team_id == next_event.team_id) or\
                       (action not in team_actions and event.team_id != next_event.team_id):
                        if action == 'in' or action == 'out':
                            action = f'sub_{action}_player_id'
                            setattr(event, action, next_event.player_id)
                    self.items.remove(next_event)
                    break
            idx += 1

    def find_related_sub(self, idx):
        event = self.items[idx]
        map_sub = {'in': 'out', 'out': 'in'}
        events = self.get_upcoming_events_at_current_time(idx)
        first_sub = None
        for ev in events:
            if ev.action_type != 'substitution' or (ev.action_type == 'substitution' and event.team_id != ev.team_id):
                continue
            if map_sub[event.sub_type] == ev.sub_type:
                if event.player_id == ev.player_id:
                    return ev
                elif not first_sub:
                    first_sub = ev
        return first_sub

    def pair_subs_at_current_time(self, idx):
        event = self.items[idx]
        events = [event]
        events += self.get_upcoming_events_at_current_time(idx)
        subs_in = [ev for ev in events if ev.action_type == 'substitution' and ev.team_id == event.team_id and ev.sub_type == 'in']
        subs_out = [ev for ev in events if ev.action_type == 'substitution' and ev.team_id == event.team_id and ev.sub_type == 'out']
        subs_in_to_remove = []
        subs_out_to_remove = []
        for sub in subs_in:
            self_sub = [ev for ev in subs_out if sub.player_id == ev.player_id]
            if len(self_sub) > 0:
                sub.sub_in_player_id = sub.player_id
                sub.sub_out_player_id = self_sub[0].player_id
                subs_out_to_remove.append(self_sub[0])
                subs_in_to_remove.append(sub)
                subs_out.remove(self_sub[0])
                delattr(sub, 'player_id')
                delattr(sub, 'sub_type')
        for sub in subs_in_to_remove:
            subs_in.remove(sub)
        if len(subs_in) != len(subs_out):
            raise Exception('You are a failure!')
        for i in range(len(subs_in)):
            subs_in[i].sub_in_player_id = subs_in[i].player_id
            subs_in[i].sub_out_player_id = subs_out[i].player_id
            delattr(subs_in[i], 'player_id')
            delattr(subs_in[i], 'sub_type')
        return subs_out_to_remove + subs_out

    def add_free_throw_count(self):
        """
        Used only by Euroleague and ACB.
        :return:
        """
        free_throws = [item for item in self.items if item.action_type == 'freethrow']
        i = 0
        while i < len(free_throws):
            shooter = free_throws[i].player_id
            sec_remaining = free_throws[i].seconds_remaining
            throws = []
            while i < len(free_throws) and free_throws[i].player_id == shooter and free_throws[i].seconds_remaining == sec_remaining:
                throws.append(free_throws[i])
                i += 1
            for j in range(len(throws)):
                throws[j].sub_type = f'{j + 1}of{len(throws)}'

    def get_previous_events_at_current_time(self, idx):
        event = self.items[idx]
        i = idx - 1
        prev_event = self.items[i]
        events = []
        while idx > 0 and (event.period == prev_event.period and event.seconds_remaining == prev_event.seconds_remaining):
            events.append(prev_event)
            i -= 1
            prev_event = self.items[i]
        return events

    def get_upcoming_events_at_current_time(self, idx):
        event = self.items[idx]
        i = idx + 1
        next_event = self.items[i]
        events = []
        while idx < len(self.items) and (
                event.period == next_event.period and event.seconds_remaining == next_event.seconds_remaining):
            events.append(next_event)
            i += 1
            next_event = self.items[i]
        return events
    def get_all_events_at_current_time(self, idx):
        events = self.get_previous_events_at_current_time(idx)
        events += self.get_upcoming_events_at_current_time(idx)
        return events

    def get_related_events(self, idx):
        """
        Used only by FIBA Live Stats and Segev Sports.
        """
        event_id = self.items[idx].event_id
        prev_event_id = self.items[idx].parent_event_id
        related = []
        prev_events = self.get_previous_events_at_current_time(idx)
        for event in prev_events:
            if event.parent_event_id == event_id or (prev_event_id != 0 and (event.parent_event_id == prev_event_id)):
                related.append(event)
        idx += 1
        while idx < len(self.items) and (self.items[idx].parent_event_id == event_id
                                         or (prev_event_id != 0 and (self.items[idx].parent_event_id == prev_event_id))):
            related.append(self.items[idx])
            idx += 1
        return related

    def _set_period_starters(self):
        pass

    def _add_score_and_margin_to_all_events(self):
        pass

    def _add_offense_team_id_to_all_events(self):
        pass