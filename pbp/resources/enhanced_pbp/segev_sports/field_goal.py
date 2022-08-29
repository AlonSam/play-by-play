import math
from typing import Optional

from pydantic import validator, conint

import pbp
from pbp.resources.enhanced_pbp import Foul, Rebound
from pbp.resources.enhanced_pbp.field_goal import FieldGoal
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem


class SegevFieldGoal(FieldGoal, SegevEnhancedPbpItem):
    """
    class for Field Goal Events
    """
    is_made: Optional[bool]
    shot_value: Optional[conint(ge=2, le=3)]
    x: Optional[float]
    y: Optional[float]
    shot_distance: Optional[float]
    is_heave: Optional[bool]
    block_player_id: Optional[int]
    assist_player_id: Optional[int]
    is_blocked_shot: Optional[bool]
    is_assisted_shot: Optional[bool]

    @validator('is_blocked_shot', always=True)
    def validate_is_blocked(cls, value, values):
        return not values['is_made'] and values['block_player_id'] is not None

    @validator('is_assisted_shot', always=True)
    def validate_is_assisted(cls, value, values):
        return values['is_made'] and values['assist_player_id'] is not None

    @validator('shot_distance', always=True)
    def validate_shot_distance(cls, value, values):
        """
        returns shot distance
        """
        if values['x'] is not None and values['y'] is not None:
            x_squared = ((values['x'] - 5) * 2) ** 2
            y_squared = (values['y'] - 50) ** 2
            shot_distance = math.sqrt(x_squared + y_squared)
            return round(shot_distance, 1)
        raise Exception('Cannot calculate distance without shot location data')

    @validator('is_heave', always=True)
    def validate_is_heave(cls, value, values):
        """
        returns True is shot was a last second heave, False otherwise
        """
        return values['shot_distance'] > pbp.HEAVE_DISTANCE_CUTOFF and values['seconds_remaining'] < pbp.HEAVE_TIME_CUTOFF

    @property
    def rebound(self) -> Rebound:
        """
        returns
        """
        if not self.is_made and isinstance(self.next_event, Rebound):
            return self.next_event

    @property
    def is_corner_3(self) -> bool:
        """
        returns True is shot was a corner 3, False otherwise
        """
        return self.shot_value == 3 and self.x <= 11

    @property
    def shot_type(self) -> str:
        """
        returns shot type string ('AtRim', 'ShortMidRange', 'LongMidRange', 'Arc3' or 'Corner3')
        """
        if self.shot_value == 3:
            if self.is_corner_3:
                return pbp.CORNER_3_STRING
            else:
                return pbp.ARC_3_STRING
        if self.shot_distance:
            if self.shot_distance < pbp.AT_RIM_CUTOFF:
                return pbp.AT_RIM_STRING
            elif self.shot_distance < pbp.SHORT_MID_RANGE_CUTOFF:
                return pbp.SHORT_MID_RANGE_STRING
            else:
                return pbp.LONG_MID_RANGE_STRING
        return pbp.UNKNOWN_SHOT_DISTANCE_STRING

    @property
    def is_putback(self) -> bool:
        """
        returns True if shot is a 2pt attempt within 2 seconds of an
        offensive rebound attempted by the same player who got the rebound
        """
        if self.is_assisted_shot or self.shot_value == 3:
            return False
        prev_ev = self.previous_event
        while prev_ev and not (isinstance(prev_ev, Rebound) and prev_ev.is_offensive):
            prev_ev = prev_ev.previous_event
        if not prev_ev:
            return False
        in_time = prev_ev.seconds_remaining - self.seconds_remaining <= 2
        return prev_ev.sub_type == 'offensive' and prev_ev.player_id == self.player_id and in_time

    @property
    def is_and_one(self) -> bool:
        if self.is_make_that_does_not_end_possession:
            return isinstance(self.next_event, Foul) and self.next_event.is_and_one_foul
        return False

    @property
    def is_make_that_does_not_end_possession(self) -> bool:
        return self.is_made and not self.is_possession_ending_event

    def get_offense_team_id(self) -> int:
        """
        returns team id that took the shot
        """
        return self.team_id

    @property
    def export_data(self):
        data = self.dict(by_alias=True, exclude_none=True, exclude={'previous_event', 'next_event'})
        data.update(self.base_data)
        data.update({
            'actionType': 'FieldGoal',
            'shotArea': self.shot_type,
            'isPutback': self.is_putback,
            'isAndOne': self.is_and_one,
            'reboundPlayerId': self.rebound.player_id if self.rebound else None
        })
        return data