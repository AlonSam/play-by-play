from typing import List, Optional

from pydantic import root_validator

import pbp
from pbp.objects.my_base_model import MyBaseModel
from pbp.resources.enhanced_pbp import (FieldGoal, FreeThrow, Rebound, Substitution, Timeout, Turnover)
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem


class EmptyPossessionError(Exception):
    pass


class Possession(MyBaseModel):
    """
    Class for possessions
    :param list events: list of
        :obj:`~pbpstats.resources.enhanced_pbp.enhanced_pbp_item.EnhancedPbpItem` items for possession,
        typically from a possession data loader
    """
    events: List[SegevEnhancedPbpItem]
    game_id: Optional[int]
    period: Optional[int]
    possession_id: Optional[int]



    @root_validator
    def add_game_id_and_period(cls, values):
        if len(values['events']) == 0:
            raise EmptyPossessionError('Possession has got no events')
        else:
            values['game_id'] = values['events'][0].game_id
            values['period'] = values['events'][0].period
        return values

    def __repr__(self):
        return (
            f"<{type(self).__name__} GameId: {self.game_id}, Period: {self.period}, "
            f"Number: {self.number}, StartTime: {self.start_time}, EndTime: {self.end_time}, "
            f"OffenseTeamId: {self.offense_team_id}>"
        )

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
            set([event.team_id for event in self.events if hasattr(event, "team_id") and event.team_id != 0]))
        prev_poss = self.previous_possession
        while len(team_ids) != 2 and prev_poss:
            team_ids += [event.team_id for event in prev_poss.events if event.team_id != 0]
            team_ids = list(set(team_ids))
            prev_poss = prev_poss.previous_possession
        next_poss = self.next_possession
        while len(team_ids) != 2 and next_poss:
            team_ids += [event.team_id for event in next_poss.events if event.team_id != 0]
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
        if self.offense_team_id == 0:
            team_ids = self.get_team_ids()
            return self.events[-1].lineup_ids[team_ids[0]]
        return self.events[-1].lineup_ids[self.offense_team_id]

    @property
    def defense_lineup_id(self):
        if self.offense_team_id == 0:
            team_ids = self.get_team_ids()
            return self.events[-1].lineup_ids[team_ids[1]]
        return self.events[-1].lineup_ids[self.defense_team_id]

    @property
    def offense_lineup_changed_during_possession(self):
        if self.offense_team_id == 0:
            return False
        return self.events[0].lineup_ids[self.offense_team_id] != self.offense_lineup_id

    @property
    def defense_lineup_changed_during_possession(self):
        if self.offense_team_id == 0:
            return False
        return self.events[0].lineup_ids[self.defense_team_id] != self.defense_lineup_id

    @property
    def possession_has_timeout(self):
        """
        returns True if there was a timeout called during the possessions, False otherwise
        """
        for i, event in enumerate(self.events):
            if isinstance(event, Timeout) and event.time != self.end_time:
                if not (event.next_event and (
                        isinstance(event.next_event, FreeThrow) and not event.next_event.is_technical_ft)
                        and event.time == event.next_event.time):
                    return True
            elif isinstance(event, Timeout) and event.time == self.end_time:
                timeout_time = event.time
                after_timeout_index = i + 1
                for possession_event in self.events[after_timeout_index:]:
                    if isinstance(possession_event, Turnover) and possession_event.time == timeout_time:
                        return True
        return False

    @property
    def previous_possession_has_timeout(self):
        """
        returns True if there was a timeout called at same time as possession started, False otherwise
        """
        if self.previous_possession:
            for event in self.previous_possession.events:
                if isinstance(event, Timeout) and event.time == self.start_time:
                    if not (event.next_event and isinstance(event.next_event,
                                                            FreeThrow) and event.time == event.next_event.time):
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
        while isinstance(self.previous_possession.events[previous_event_index], Substitution) \
                and len(self.previous_possession.events) > abs(previous_event_index):
            previous_event_index -= 1
        return self.previous_possession.events[previous_event_index]

    @property
    def possession_start_type(self):
        """
        returns possession start type string
        """
        if self.possession_id == 1:
            return pbp.OFF_DEADBALL_STRING
        if self.possession_has_timeout or self.previous_possession_has_timeout:
            return pbp.OFF_TIMEOUT_STRING
        if isinstance(self.previous_possession_ending_event, (FieldGoal, FreeThrow)) and self.previous_possession_ending_event.is_made:
            shot_type = self.previous_possession_ending_event.shot_type
            return f'Off{shot_type}{pbp.MAKE_STRING}'
        if isinstance(self.previous_possession_ending_event, Turnover):
            if self.previous_possession_ending_event.is_steal:
                return pbp.OFF_LIVE_BALL_TURNOVER_STRING
            return pbp.OFF_DEADBALL_STRING
        if isinstance(self.previous_possession_ending_event, Rebound):
            if self.previous_possession_ending_event.player_id == 0:
                return pbp.OFF_DEADBALL_STRING
            missed_shot = self.previous_possession_ending_event.missed_shot
            shot_type = missed_shot.shot_type
            if missed_shot.is_blocked:
                return f'Off{shot_type}{pbp.BLOCK_STRING}'
            return f'Off{shot_type}{pbp.MISS_STRING}'
        return pbp.OFF_DEADBALL_STRING

    @property
    def previous_possession_end_shooter_player_id(self):
        """
        return player id of player who took shot (make or miss) that ended previous possession.
        returns 0 if previous possession did not end with made field goal or live ball rebound
        """
        if self.previous_possession and (self.possession_has_timeout or self.previous_possession_has_timeout):
            if isinstance(self.previous_possession_ending_event, FieldGoal) and self.previous_possession_ending_event.is_made:
                return self.previous_possession_ending_event.player_id
            if isinstance(self.previous_possession_ending_event, Rebound):
                if self.previous_possession_ending_event.player_id != 0:
                    return self.previous_possession_ending_event.missed_shot.player_id

    @property
    def previous_possession_end_rebound_player_id(self):
        """
        returns player id of player who got rebound that ended previous possession.
        returns 0 if previous possession did not end with a live ball rebound
        """
        if self.previous_possession and not (self.possession_has_timeout or self.previous_possession_has_timeout):
            if isinstance(self.previous_possession_ending_event, Rebound):
                return self.previous_possession_ending_event.player_id

    @property
    def previous_possession_end_steal_player_id(self):
        """
        returns player id of player who got steal that ended previous possession.
        returns 0 if previous possession did not end with a live ball turnover
        """
        if self.previous_possession and not (self.possession_has_timeout or self.previous_possession_has_timeout):
            if isinstance(self.previous_possession_ending_event, Turnover):
                if self.previous_possession_ending_event.is_steal:
                    return self.previous_possession_ending_event.steal_player_id

    @property
    def data(self):
        return self.__dict__

    @property
    def export_data(self):
        exclude = {'previous_possession', 'next_possession', 'events'}
        data = self.dict(by_alias=True, exclude_none=True, exclude=exclude)
        data.update({
            'events': [e.export_data for e in self.events],
            'offenseTeamId': self.offense_team_id,
            'defenseTeamId': self.defense_team_id,
            'offenseLineupId': self.offense_lineup_id,
            'defenseLineupId': self.defense_lineup_id,
            'offenseLineupChanged': self.offense_lineup_changed_during_possession,
            'defenseLineupChanged': self.defense_lineup_changed_during_possession,
            'startTime': self.start_time,
            'endTime': self.end_time,
            'duration': self.duration,
            'startScore': self.score,
            'startScoreMargin': self.margin,
            'hasTimeout': self.possession_has_timeout,
            'previousPossessionEndingEventId': self.previous_possession_ending_event.event_id if self.previous_possession else None,
            'previousPossessionEndReboundPlayerId': self.previous_possession_end_rebound_player_id,
            'previousPossessionEndShooterPlayerId': self.previous_possession_end_shooter_player_id,
            'previousPossessionEndStealPlayerId': self.previous_possession_end_steal_player_id
        })
        return {k: v for (k, v) in data.items() if v is not None}
