import pbp
from pbp.models.events.field_goal import FieldGoalEvent
from pbp.models.events.free_throw import FreeThrowEvent
from pbp.models.events.rebound import ReboundEvent
from pbp.models.events.substitution import SubstitutionEvent
from pbp.models.events.timeout import TimeoutEvent
from pbp.models.events.turnover import TurnoverEvent


class EmptyPossessionError(Exception):
    pass


class PossessionItem(object):
    """
    Class for possessions
    :param list events: list of
        :obj:`~pbpstats.resources.enhanced_pbp.enhanced_pbp_item.EnhancedPbpItem` items for possession,
        typically from a possession data loader
    """
    def __init__(self, events):
        self.events = events

    @property
    def game_id(self):
        return self.events[0].game_id

    @property
    def period(self):
        return self.events[0].period

    @property
    def start_time(self):
        """
        returns the time remaining (MM:SS) in the period when the possession started
        """
        if not hasattr(self, "previous_possession") or not self.previous_possession:
            return self.events[0].time
        return self.previous_possession.events[-1].time

    @property
    def end_time(self):
        """
        returns the time remaining (MM:SS) in the period when the possession ended
        """
        return self.events[-1].time

    @property
    def duration(self):
        if not hasattr(self, "previous_possession") or not self.previous_possession:
            start_time = self.events[0].seconds_remaining
        else:
            start_time = self.previous_possession.events[-1].seconds_remaining
        end_time = self.events[-1].seconds_remaining
        return start_time - end_time

    @property
    def margin(self):
        """
        returns the score margin from the perspective of the team on offense when the possession started
        """
        first_event = self.events[0]
        if first_event.team_id == first_event.offense_team_id:
            return first_event.margin
        return first_event.margin * -1

    @property
    def score(self):
        """
        returns the score when possession started
        """
        return self.events[0].score

    def get_team_ids(self):
        """
        returns a list with the team ids fo both teams playing
        """
        team_ids = list(
            set([event.team_id for event in self.events if hasattr(event, "team_id") and event.team_id != '0']))
        prev_poss = self.previous_possession
        while len(team_ids) != 2 and prev_poss:
            team_ids += [event.team_id for event in prev_poss.events if event.team_id != '0']
            team_ids = list(set(team_ids))
            prev_poss = prev_poss.previous_possession
        next_poss = self.next_possession
        while len(team_ids) != 2 and next_poss:
            team_ids += [event.team_id for event in next_poss.events if event.team_id != '0']
            team_ids = list(set(team_ids))
            next_poss = next_poss.next_possession
        return team_ids

    @property
    def offense_team_id(self):
        return self.events[0].offense_team_id

    @property
    def defense_team_id(self):
        team_ids = self.get_team_ids()
        return team_ids[0] if self.offense_team_id == team_ids[1] else team_ids[1]

    @property
    def offense_lineup_id(self):
        if self.offense_team_id == '0':
            team_ids = self.get_team_ids()
            return self.events[-1].lineup_ids[team_ids[0]]
        if self.offense_lineup_changed_during_possession and self.possession_ends_with_ft:
            return self.events[0].lineup_ids[self.offense_team_id]
        return self.events[-1].lineup_ids[self.offense_team_id]

    @property
    def defense_lineup_id(self):
        if self.offense_team_id == '0':
            team_ids = self.get_team_ids()
            return self.events[-1].lineup_ids[team_ids[1]]
        if self.defense_lineup_changed_during_possession and self.possession_ends_with_ft:
            return self.events[0].lineup_ids[self.defense_team_id]
        return self.events[-1].lineup_ids[self.defense_team_id]

    @property
    def offense_lineup_changed_during_possession(self):
        if self.offense_team_id == '0':
            return False
        return self.events[0].lineup_ids[self.offense_team_id] != self.events[-1].lineup_ids[self.offense_team_id]

    @property
    def defense_lineup_changed_during_possession(self):
        if self.offense_team_id == '0':
            return False
        return self.events[0].lineup_ids[self.defense_team_id] != self.events[-1].lineup_ids[self.defense_team_id]

    @property
    def possession_ends_with_ft(self):
        if isinstance(self.events[-1], FreeThrowEvent):
            return True
        if isinstance(self.events[-1], ReboundEvent) and self.events[-1].missed_shot_type == 'FreeThrow':
            return True
        return False

    @property
    def is_over_the_limit(self):
        return self.events[0].fouls_to_give[self.defense_team_id] == 0

    @property
    def possession_has_timeout(self):
        """
        returns True if there was a timeout called during the possessions, False otherwise
        """
        for i, event in enumerate(self.events):
            if isinstance(event, TimeoutEvent) and event.time != self.end_time:
                if not (event.next_event and (
                        isinstance(event.next_event, FreeThrowEvent) and not event.next_event.is_technical_ft)
                        and event.time == event.next_event.time):
                    return True
            elif isinstance(event, TimeoutEvent) and event.time == self.end_time:
                timeout_time = event.time
                after_timeout_index = i + 1
                for possession_event in self.events[after_timeout_index:]:
                    if isinstance(possession_event, TurnoverEvent) and possession_event.time == timeout_time:
                        return True
        return False

    @property
    def previous_possession_has_timeout(self):
        """
        returns True if there was a timeout called at same time as possession started, False otherwise
        """
        if self.previous_possession:
            previous_possession_events = self.previous_possession.events
            for i, event in enumerate(previous_possession_events):
                if isinstance(event, TimeoutEvent) and event.time == self.start_time:
                    if i == len(previous_possession_events) - 1:
                        return True
                    j = i + 1
                    next_event = previous_possession_events[j]
                    while j + 1 < len(previous_possession_events) and isinstance(next_event, SubstitutionEvent)\
                            and event.time == next_event.time:
                        j += 1
                        next_event = previous_possession_events[j]
                    if not (isinstance(next_event, FreeThrowEvent) and event.time == next_event.time):
                        return True
        return False

    @property
    def previous_possession_ending_event(self):
        """
        returns previous possession ending event - ignoring subs
        """
        if not self.previous_possession:
            return
        previous_event_index = -1
        while isinstance(self.previous_possession.events[previous_event_index], SubstitutionEvent) \
                and len(self.previous_possession.events) > abs(previous_event_index):
            previous_event_index -= 1
        return self.previous_possession.events[previous_event_index]

    @property
    def possession_start_type(self):
        """
        returns possession start type string
        """
        if self.possession_id.endswith('001'):
            return pbp.OFF_DEADBALL_STRING
        if self.possession_has_timeout or self.previous_possession_has_timeout:
            return pbp.OFF_TIMEOUT_STRING
        if isinstance(self.previous_possession_ending_event,
                      (FieldGoalEvent, FreeThrowEvent)) and self.previous_possession_ending_event.is_made:
            if isinstance(self.previous_possession_ending_event, FieldGoalEvent):
                shot_type = self.previous_possession_ending_event.shot_type
                return f'Off{shot_type}{pbp.MAKE_STRING}'
            return f'Off{pbp.FREE_THROW_STRING}{pbp.MAKE_STRING}'
        if isinstance(self.previous_possession_ending_event, TurnoverEvent):
            if self.previous_possession_ending_event.is_steal:
                return pbp.OFF_LIVE_BALL_TURNOVER_STRING
            return pbp.OFF_DEADBALL_STRING
        if isinstance(self.previous_possession_ending_event, ReboundEvent):
            if self.previous_possession_ending_event.player_id == 0:
                return pbp.OFF_DEADBALL_STRING
            missed_shot_event_id = self.previous_possession_ending_event.missed_shot_event_id
            for event in self.previous_possession.events:
                if event.event_id == missed_shot_event_id:
                    missed_shot = event
                    break
            if hasattr(missed_shot, 'shot_type'):
                shot_type = missed_shot.shot_type
                if missed_shot.is_blocked:
                    return f'Off{shot_type}{pbp.BLOCK_STRING}'
                return f'Off{shot_type}{pbp.MISS_STRING}'
            return f'Off{pbp.FREE_THROW_STRING}{pbp.MISS_STRING}'
        return pbp.OFF_DEADBALL_STRING


    @property
    def previous_possession_end_shooter_player_id(self):
        """
        return player id of player who took shot (make or miss) that ended previous possession.
        returns 0 if previous possession did not end with made field goal or live ball rebound
        """
        if self.previous_possession and (self.possession_has_timeout or self.previous_possession_has_timeout):
            if isinstance(self.previous_possession_ending_event,
                          FieldGoalEvent) and self.previous_possession_ending_event.is_made:
                return self.previous_possession_ending_event.player_id
            if isinstance(self.previous_possession_ending_event, ReboundEvent):
                if self.previous_possession_ending_event.player_id != 0:
                    return self.previous_possession_ending_event.missed_shot.player_id

    @property
    def previous_possession_end_rebound_player_id(self):
        """
        returns player id of player who got rebound that ended previous possession.
        returns 0 if previous possession did not end with a live ball rebound
        """
        if self.previous_possession and not (self.possession_has_timeout or self.previous_possession_has_timeout):
            if isinstance(self.previous_possession_ending_event, ReboundEvent) and not self.previous_possession_ending_event.is_team_rebound:
                return self.previous_possession_ending_event.player_id

    @property
    def previous_possession_end_steal_player_id(self):
        """
        returns player id of player who got steal that ended previous possession.
        returns 0 if previous possession did not end with a live ball turnover
        """
        if self.previous_possession and not (self.possession_has_timeout or self.previous_possession_has_timeout):
            if isinstance(self.previous_possession_ending_event, TurnoverEvent):
                if self.previous_possession_ending_event.is_steal:
                    return self.previous_possession_ending_event.steal_player_id

    @property
    def data(self):
        return self.__dict__
