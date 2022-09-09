"""
will load pbp from each resource and convert to same pattern
"""


class EnhancedPbpLoader(object):
    """
    Base class for all EnhancedPbpLoaders.
    This class should not be instantiated directly.
    """

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

    def pair_subs_at_current_time(self, idx):
        sub = self.raw_events[idx]
        subs = [sub]
        subs += self.get_subs_at_current_time(idx, sub.team_id)
        subs_in = [ev for ev in subs if ev.team_id == sub.team_id and ev.sub_type == 'in']
        subs_out = [ev for ev in subs if ev.team_id == sub.team_id and ev.sub_type == 'out']
        combined_subs = []
        subs_in_to_remove = []
        for sub in subs_in:
            self_sub = self.get_self_sub(subs_out, sub.player_id)
            if self_sub:
                # combined_sub = self.create_combined_sub(sub, self_sub)
                # combined_subs.append(combined_sub)
                subs_in_to_remove.append(sub)
                subs_out.remove(self_sub)
        subs_in = [sub for sub in subs_in if sub not in subs_in_to_remove]
        for i in range(len(subs_in)):
            combined_sub = self.create_combined_sub(subs_in[i], subs_out[i])
            combined_subs.append(combined_sub)
        return combined_subs, subs

    def get_subs_at_current_time(self, idx, team_id):
        event = self.raw_events[idx]
        i = idx + 1
        next_event = self.raw_events[i]
        events = []
        while idx < len(self.raw_events) and (
                event.period == next_event.period and event.seconds_remaining == next_event.seconds_remaining):
            if next_event.team_id == team_id and next_event.action_type == 'substitution':
                events.append(next_event)
            i += 1
            next_event = self.raw_events[i]
        return events

    @staticmethod
    def create_combined_sub(sub_in, sub_out):
        combined_sub = sub_in.copy()
        combined_sub.sub_in_player_id = sub_in.player_id
        combined_sub.sub_out_player_id = sub_out.player_id
        delattr(combined_sub, 'player_id')
        delattr(combined_sub, 'sub_type')
        return combined_sub

    @staticmethod
    def get_self_sub(subs, player_id):
        for sub in subs:
            if sub.player_id == player_id:
                return sub


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
        event = self.raw_events[idx]
        i = idx - 1
        prev_event = self.raw_events[i]
        events = []
        while idx > 0 and (event.period == prev_event.period and event.seconds_remaining == prev_event.seconds_remaining):
            events.append(prev_event)
            i -= 1
            prev_event = self.raw_events[i]
        return events

    def get_upcoming_events_at_current_time(self, idx):
        event = self.raw_events[idx]
        i = idx + 1
        next_event = self.raw_events[i]
        events = []
        while idx < len(self.raw_events) and (
                event.period == next_event.period and event.seconds_remaining == next_event.seconds_remaining):
            events.append(next_event)
            i += 1
            next_event = self.raw_events[i]
        return events

    def get_all_events_at_current_time(self, idx):
        events = self.get_previous_events_at_current_time(idx)
        events += self.get_upcoming_events_at_current_time(idx)
        return events

    def get_related_events(self, idx):
        """
        Used only by FIBA Live Stats and Segev Sports.
        """
        event_id = self.raw_events[idx].event_id
        prev_event_id = self.raw_events[idx].parent_event_id
        related = []
        prev_events = self.get_previous_events_at_current_time(idx)
        for event in prev_events:
            if event.parent_event_id == event_id or (prev_event_id != 0 and (event.parent_event_id == prev_event_id)):
                related.append(event)
        idx += 1
        while idx < len(self.raw_events) and (self.raw_events[idx].parent_event_id == event_id
                                         or (prev_event_id != 0 and (self.raw_events[idx].parent_event_id == prev_event_id))):
            related.append(self.raw_events[idx])
            idx += 1
        return related