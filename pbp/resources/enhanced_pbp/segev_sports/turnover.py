from typing import Optional

from pydantic import validator

from pbp.resources.enhanced_pbp import Foul
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem
from pbp.resources.enhanced_pbp.turnover import Turnover


class SegevTurnover(Turnover, SegevEnhancedPbpItem):
    steal_player_id: Optional[int]
    is_steal: Optional[bool]

    @validator('is_steal', always=True)
    def validate_is_steal(cls, value, values):
        return values['steal_player_id'] is not None

    @property
    def is_bad_pass(self):
        return self.sub_type == 'badpass'

    @property
    def is_ball_handling(self):
        return self.sub_type == 'ballhandling'

    @property
    def is_travel(self):
        return self.sub_type == 'travel'

    @property
    def is_shot_clock_violation(self):
        return self.sub_type == '24sec'

    @property
    def is_offensive_goaltending(self):
        return self.sub_type == 'offensivegoaltending'

    @property
    def is_lane_violation(self):
        return self.sub_type == 'laneviolation'

    @property
    def is_3_second_violation(self):
        return self.sub_type == '3sec'

    @property
    def is_5_second_violation(self):
        return self.sub_type == '5sec'

    @property
    def is_8_second_violation(self):
        return self.sub_type == '8sec'

    @property
    def is_out_of_bounds(self):
        return self.sub_type == 'outofbounds'

    @property
    def is_offensive_foul(self):
        return self.sub_type == 'other' and isinstance(self.previous_event, Foul) and self.previous_event.is_offensive_foul

    @property
    def is_backcourt_violation(self):
        return self.sub_type == 'backcourt'

    @property
    def is_double_dribble(self):
        return self.sub_type == 'doubledribble'

    @property
    def is_unknown(self):
        return self.sub_type == 'other' and not self.is_offensive_foul

    @property
    def export_data(self):
        data = self.dict(by_alias=True, exclude_none=True, exclude={'previous_event', 'next_event'})
        data.update(self.base_data)
        return data