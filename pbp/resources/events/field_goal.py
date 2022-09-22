from abc import abstractmethod
from typing import List

import numpy as np

import pbp
from models.db.stats_model import StatsModel
from pbp.exceptions import ReboundNotFound, ShotLocationUnknown


class FieldGoal(object):
    """
    Class for field goal events
    """
    event_type = ['2pt', '3pt']

    @property
    @abstractmethod
    def is_assisted(self):
        pass

    @property
    @abstractmethod
    def is_blocked(self):
        pass

    @property
    def shot_distance(self) -> float:
        """
        returns the shot distance in metres if coordinates exist, raises Exception otherwise.
        """
        if self.x is not None and self.y is not None:
            rim_location = np.array([250.0, 52.5])
            location = np.array([self.x, self.y])
            shot_distance = np.linalg.norm(location - rim_location)
            shot_distance_in_metres = shot_distance / (500 / 15)
            return round(shot_distance_in_metres, 1)
        raise ShotLocationUnknown('Cannot calculate distance without shot location data')

    @property
    def is_corner_3(self) -> bool:
        """
        returns True is shot was a corner 3, False otherwise
        """
        return self.shot_value == 3 and self.y < 94.167

    @property
    def basic_shot_zone(self) -> str:
        """
        returns shot type string ('AtRim', 'ShortMidRange', 'LongMidRange', 'Arc3' or 'Corner3')
        """
        if self.shot_value == 3:
            if self.is_corner_3:
                return pbp.CORNER_3_STRING
            else:
                return pbp.ABOVE_THE_BREAK_3_STRING
        if self.shot_distance is not None:
            if self.shot_distance < pbp.AT_RIM_CUTOFF:
                return pbp.AT_RIM_STRING
            elif pbp.PAINT_RIGHT_X < self.x < pbp.PAINT_LEFT_X and pbp.PAINT_BOTTOM_Y < self.y < pbp.PAINT_UPPER_Y:
                return pbp.PAINT_STRING
            else:
                return pbp.MID_RANGE_STRING
        return pbp.UNKNOWN_SHOT_DISTANCE_STRING

    @property
    def shot_zone(self) -> str:
        """
        returns advanced shot zone ('AtRim, 'Paint', 'LeftCornerMidRange', 'LeftWingMidRange', 'CenterMidRange',
        'RightWingMidRange', 'RightCornerMidRange', 'RightCorner3', 'LeftCorner3', 'RightWing3', 'LeftWing3', 'Center3'
        :return:
        """
        if self.shot_value == 3:
            if self.is_corner_3:
                if self.x > 250:
                    return pbp.LEFT_CORNER_3_STRING
                else:
                    return pbp.RIGHT_CORNER_3_STRING
            elif pbp.LEFT_WING_LINE(self.x) > self.y:
                return pbp.LEFT_WING_3_STRING
            elif pbp.RIGHT_WING_LINE(self.x) > self.y:
                return pbp.RIGHT_WING_3_STRING
            else:
                return pbp.CENTER_3_STRING
        else:
            if self.shot_distance < pbp.AT_RIM_CUTOFF:
                return pbp.AT_RIM_STRING
            elif pbp.PAINT_RIGHT_X < self.x < pbp.PAINT_LEFT_X and pbp.PAINT_BOTTOM_Y < self.y < pbp.PAINT_UPPER_Y:
                return pbp.PAINT_STRING
            elif self.y < pbp.CORNER_MID_RANGE_UPPER_Y:
                if self.x < 250:
                    return pbp.RIGHT_CORNER_MID_RANGE_STRING
                else:
                    return pbp.LEFT_CORNER_MID_RANGE_STRING
            elif pbp.LEFT_WING_LINE(self.x) > self.y:
                return pbp.LEFT_WING_MID_RANGE_STRING
            elif pbp.RIGHT_WING_LINE(self.x) > self.y:
                return pbp.RIGHT_WING_3_STRING
            else:
                return pbp.CENTER_MID_RANGE_STRING

    @property
    def is_heave(self) -> bool:
        """
        returns True if shot was taken at the last 2 seconds of a period and from an unreasonable distance
        """
        return self.shot_distance > pbp.HEAVE_DISTANCE_CUTOFF and self.seconds_remaining <= pbp.HEAVE_TIME_CUTOFF

    @property
    def rebound(self):
        """
        returns a :obj:`~pbp.resources.events.rebound.Rebound` object if shot was missed, None otherwise
        """
        if not self.is_made:
            next_event = self.next_event
            while next_event and next_event.action_type == 'substitution':
                next_event = next_event.next_event
            if next_event.action_type == 'rebound':
                return next_event
            if next_event.action_type == 'endofquarter':
                return None
            if next_event.action_type == 'turnover' and next_event.is_shot_clock_violation:
                return None
            if next_event.action_type == 'timeout':
                while next_event and next_event.action_type != 'rebound':
                    next_event = next_event.next_event
                if next_event.seconds_remaing == self.seconds_remaining:
                    return next_event
                raise ReboundNotFound(f'{self.game_id}-Q{self.period}-{self.time}')

            if next_event.action_type == 'foul' and next_event.is_offensive_foul:
                while next_event and next_event.action_type != 'rebound':
                    next_event = next_event.next_event
                if next_event.parent_event_id == self.event_id:
                    return next_event
                else:
                    raise ReboundNotFound(f'{self.game_id}-Q{self.period}-{self.time}')
            raise ReboundNotFound(f'{self.game_id}-Q{self.period}-{self.time}')

    @property
    def rebound_event_id(self) -> str:
        """
        returns the `event_id` attribute of the :obj:`~pbp.resources.events.rebound.Rebound` if exists, None otherwise.
        """
        return self.rebound.event_id if self.rebound else None

    @property
    def is_make_that_does_not_end_possession(self) -> bool:
        """
        returns True if shot was made but did not end the possession, False otherwise
        """
        return self.is_made and not self.is_possession_ending_event

    @property
    def event_stats(self) -> List[StatsModel]:
        """
        returns list of StatsModel object with all stats for event
        """
        stats_models = []
        stat_keys = []
        if self.shot_distance is not None:
            if self.shot_value == 2:
                distance_stat_key = pbp.TOTAL_2PT_SHOT_DISTANCE_STRING
                count_stat_keys = pbp.TOTAL_2PT_SHOTS_WITH_DISTANCE
            else:
                distance_stat_key = pbp.TOTAL_3PT_SHOT_DISTANCE_STRING
                count_stat_keys = pbp.TOTAL_3PT_SHOTS_WITH_DISTANCE
            stats_models.append(
                StatsModel(
                    player_id=self.player_id,
                    team_id=self.team_id,
                    stat_key=distance_stat_key,
                    stat_value=self.shot_distance
                )
            )
            stat_keys.append(count_stat_keys)
            if self.is_heave:
                heave_attempt_stat_key = pbp.HEAVE_STRING + pbp.ATTEMPTS_STRING
                if self.is_made:
                    heave_stat_key = pbp.HEAVE_STRING + pbp.MAKES_STRING
                    stat_keys.append(heave_stat_key)
                stat_keys.append(heave_attempt_stat_key)
        assist_keys = []
        attempt_key = f'{self.shot_zone}{pbp.ATTEMPTS_STRING}'
        stat_keys.append(attempt_key)
        stat_keys += self._add_misc_stats(attempt_key)
        if self.is_made:
            if self.is_assisted:
                scorer_key = f'{pbp.ASSISTED_STRING}{self.shot_zone}'
                assist_key = f'{self.shot_zone}{pbp.ASSISTS_STRING}'
                stat_keys.append(scorer_key)
                assist_keys.append(assist_key)
                stat_keys += self._add_misc_stats(scorer_key)
                assist_keys += self._add_misc_stats(assist_key)
                assist_keys.append(f'{self.assist_player_id}-To-{self.player_id}-{self.shot_zone}-Assists')
                for key in assist_keys:
                    stats_models.append(
                        StatsModel(
                            player_id=self.assist_player_id,
                            team_id=self.team_id,
                            stat_key=key,
                            stat_value=1
                        )
                    )
            else:
                stat_key = f'{pbp.UNASSISTED_STRING}{self.shot_zone}'
                stat_keys.append(stat_key)
                stat_keys += self._add_misc_stats(stat_key)
                if self.is_putback:
                    stat_keys.append(pbp.PUTBACKS_STRING)
        else:
            if self.is_blocked:
                block_keys = []
                miss_key = f'{pbp.BLOCKED_STRING}{self.basic_shot_zone}'
                block_key = f'{self.basic_shot_zone}{pbp.BLOCKS_STRING}'
                block_keys.append(block_key)
                stat_keys += self._add_misc_stats(miss_key)
                block_keys += self._add_misc_stats(block_key)
                for key in block_keys:
                    stats_models.append(
                        StatsModel(
                            player_id=self.block_player_id,
                            team_id=self.team_id,
                            stat_key=key,
                            stat_value=1
                        )
                    )
        for stat_key in stat_keys:
            stats_models.append(
                StatsModel(
                    player_id=self.player_id,
                    team_id=self.team_id,
                    stat_key=stat_key,
                    stat_value=1
                )
            )
        stats_models = self._add_lineup_data(stats_models)
        return self.base_stats + stats_models

