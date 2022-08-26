from pbp.resources.enhanced_pbp import Foul
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem
from pbp.resources.enhanced_pbp.turnover import Turnover


class SegevTurnover(Turnover, SegevEnhancedPbpItem):
    @property
    def is_steal(self):
        return hasattr(self, 'steal_player_id')

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
        data = {
            'action_type': 'Turnover',
            'type': self.sub_type,
            'is_steal': self.is_steal,
            'steal_player_id': self.steal_player_id if self.is_steal else 0
        }
        base_data = self.base_data.copy()
        base_data.update(data)
        return base_data