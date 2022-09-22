from itertools import groupby
from operator import itemgetter

import pbp
from models.db.stats_model import StatsModel
from pbp.models.db.events import *


class PossessionItem(object):
    """
    Class for possessions
    :param list events: list of
        :obj:`~pbpstats.resources.events.enhanced_pbp_item.EnhancedPbpItem` items for possession,
        typically from a possession data loader
    """
    def __init__(self, events):
        self.events = events
        self.previous_possession = None
        self.previous_possession_id = None
        self.next_possession = None
        self.next_possession_id = None

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
        if self.previous_possession is None or isinstance(self.previous_possession.events[-1], EndOfPeriodEventModel):
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
        if self.previous_possession is None or isinstance(self.previous_possession.events[-1], EndOfPeriodEventModel):
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

    @property
    def offense_team_id(self):
        return self.events[0].offense_team_id

    @property
    def defense_team_id(self):
        return self.team_ids[0] if self.offense_team_id == self.team_ids[1] else self.team_ids[1]

    @property
    def offense_lineup_id(self):
        if self.offense_team_id == '0':
            return self.events[-1].lineup_ids[self.team_ids[0]]
        if self.offense_lineup_changed_during_possession and self.possession_ends_with_ft:
            return self.events[0].lineup_ids[self.offense_team_id]
        return self.events[-1].lineup_ids[self.offense_team_id]

    @property
    def defense_lineup_id(self):
        if self.offense_team_id == '0':
            return self.events[-1].lineup_ids[self.team_ids[1]]
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
        if isinstance(self.events[-1], FreeThrowEventModel):
            return True
        if isinstance(self.events[-1], ReboundEventModel) and self.events[-1].missed_shot_zone == 'FreeThrow':
            return True
        return False

    @property
    def is_over_the_limit(self):
        return self.events[0].fouls_to_give[self.defense_team_id] == 0

    @property
    def possession_has_timeout(self):
        """
        returns True if there was a timeout called during the possession, False otherwise
        """
        for i, event in enumerate(self.events):
            if isinstance(event, TimeoutEventModel) and event.time != self.end_time:
                next_event = self.events[i + 1]
                if not (isinstance(next_event, FreeThrowEventModel) and not next_event.is_technical_ft
                    and next_event.time == event.time):
                    return True
            elif isinstance(event, TimeoutEventModel) and event.time == self.end_time:
                timeout_time = event.time
                after_timeout_index = i + 1
                for possession_event in self.events[after_timeout_index:]:
                    if isinstance(possession_event, TurnoverEventModel) and possession_event.time == timeout_time:
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
                if isinstance(event, TimeoutEventModel) and event.time == self.start_time:
                    if i == len(previous_possession_events) - 1:
                        return True
                    j = i + 1
                    next_event = previous_possession_events[j]
                    while j + 1 < len(previous_possession_events) and isinstance(next_event, SubstitutionEventModel)\
                            and event.time == next_event.time:
                        j += 1
                        next_event = previous_possession_events[j]
                    if not (isinstance(next_event, FreeThrowEventModel) and event.time == next_event.time):
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
        while isinstance(self.previous_possession.events[previous_event_index], SubstitutionEventModel) \
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
                      (FieldGoalEventModel, FreeThrowEventModel)) and self.previous_possession_ending_event.is_made:
            if isinstance(self.previous_possession_ending_event, FieldGoalEventModel):
                shot_zone = self.previous_possession_ending_event.shot_zone
                return f'Off{shot_zone}{pbp.MAKE_STRING}'
            return f'Off{pbp.FREE_THROW_STRING}{pbp.MAKE_STRING}'
        if isinstance(self.previous_possession_ending_event, TurnoverEventModel):
            if self.previous_possession_ending_event.is_steal:
                return pbp.OFF_LIVE_BALL_TURNOVER_STRING
            return pbp.OFF_DEADBALL_STRING
        if isinstance(self.previous_possession_ending_event, ReboundEventModel):
            if self.previous_possession_ending_event.player_id == 0:
                return pbp.OFF_DEADBALL_STRING
            missed_shot_event_id = self.previous_possession_ending_event.missed_shot_event_id
            for event in self.previous_possession.events:
                if event.event_id == missed_shot_event_id:
                    missed_shot = event
                    break
            if hasattr(missed_shot, 'shot_zone'):
                shot_zone = missed_shot.shot_zone
                if missed_shot.is_blocked:
                    return f'Off{shot_zone}{pbp.BLOCK_STRING}'
                return f'Off{shot_zone}{pbp.MISS_STRING}'
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
                          FieldGoalEventModel) and self.previous_possession_ending_event.is_made:
                return self.previous_possession_ending_event.player_id
            if isinstance(self.previous_possession_ending_event, ReboundEventModel):
                if self.previous_possession_ending_event.player_id != 0:
                    return self.previous_possession_ending_event.missed_shot.player_id

    @property
    def previous_possession_end_rebound_player_id(self):
        """
        returns player id of player who got rebound that ended previous possession.
        returns 0 if previous possession did not end with a live ball rebound
        """
        if self.previous_possession and not (self.possession_has_timeout or self.previous_possession_has_timeout):
            if isinstance(self.previous_possession_ending_event, ReboundEventModel) and not self.previous_possession_ending_event.is_team_rebound:
                return self.previous_possession_ending_event.player_id

    @property
    def previous_possession_end_steal_player_id(self):
        """
        returns player id of player who got steal that ended previous possession.
        returns 0 if previous possession did not end with a live ball turnover
        """
        if self.previous_possession and not (self.possession_has_timeout or self.previous_possession_has_timeout):
            if isinstance(self.previous_possession_ending_event, TurnoverEventModel):
                if self.previous_possession_ending_event.is_steal:
                    return self.previous_possession_ending_event.steal_player_id

    @property
    def possession_stats(self):
        grouper = itemgetter(
            "player_id",
            "team_id",
            "opponent_team_id",
            "lineup_id",
            "opponent_lineup_id",
            "stat_key",
        )
        results = []
        event_stats = [
            event_stat.dict() for event in self.events for event_stat in event.event_stats
        ]
        for key, group in groupby(sorted(event_stats, key=grouper), grouper):
            temp_dict = dict(
                zip(
                    [
                        "player_id",
                        "team_id",
                        "opponent_team_id",
                        "lineup_id",
                        "opponent_lineup_id",
                        "stat_key",
                    ],
                    key,
                )
            )
            temp_dict["stat_value"] = sum(item["stat_value"] for item in group)
            results.append(StatsModel(**temp_dict))
        points_scored = self.events[-1].score[self.offense_team_id] - self.score[self.offense_team_id]
        names = ['offense', 'defense']
        for name in names:
            team_id = getattr(self, f'{name}_team_id')
            opponent_team_id = self.defense_team_id if team_id == self.offense_team_id else self.offense_team_id
            lineup_id = getattr(self, f'{name}_lineup_id')
            opponent_lineup_id = self.defense_lineup_id if lineup_id == self.offense_lineup_id else self.offense_lineup_id
            lineup = lineup_id.split('-')
            possession_stat_key = pbp.OFFENSIVE_POSSESSION_STRING if name == 'offense' else pbp.DEFENSIVE_POSSESSION_STRING
            for player_id in lineup:
                results.append(
                    StatsModel(
                        player_id=player_id,
                        team_id=team_id,
                        opponent_team_id=opponent_team_id,
                        lineup_id=lineup_id,
                        opponent_lineup_id=opponent_lineup_id,
                        stat_key=possession_stat_key,
                        stat_value=1
                    )
                )
                if points_scored > 0:
                    multiplier = 1 if name == 'offense' else -1
                    results.append(
                        StatsModel(
                            player_id=player_id,
                            team_id=team_id,
                            opponent_team_id=opponent_team_id,
                            lineup_id=lineup_id,
                            opponent_lineup_id=opponent_lineup_id,
                            stat_key=pbp.PLUS_MINUS_STRING,
                            stat_value=points_scored * multiplier
                        )
                    )
                    score_stat_key = pbp.TEAM_POINTS if name == 'offense' else pbp.OPPONENT_POINTS
                    results.append(
                        StatsModel(
                            player_id=player_id,
                            team_id=team_id,
                            opponent_team_id=opponent_team_id,
                            lineup_id=lineup_id,
                            opponent_lineup_id=opponent_lineup_id,
                            stat_key=score_stat_key,
                            stat_value=points_scored
                        )
                    )
        return results

    @property
    def data(self):
        return self.__dict__
