from pydantic import root_validator, ValidationError

from .event_model import EventModel


class TurnoverEventModel(EventModel):
    is_steal: bool
    steal_player_id: str = None
    is_3_second_violation: bool
    is_5_second_violation: bool
    is_8_second_violation: bool
    is_backcourt_violation: bool
    is_bad_pass: bool
    is_ball_handling: bool
    is_double_dribble: bool
    is_offensive_foul: bool
    is_out_of_bounds: bool
    is_shot_clock_violation: bool
    is_travel: bool
    is_unknown: bool

    @root_validator
    def validate_has_type(cls, values):
        types = ['is_3_second_violation', 'is_5_second_violation', 'is_8_second_violation', 'is_backcourt_violation',
                 'is_bad_pass', 'is_ball_handling', 'is_double_dribble', 'is_offensive_foul', 'is_lane_violation',
                 'is_out_of_bounds', 'is_shot_clock_violation', 'is_travel', 'is_unknown']
        for turnover_type in types:
            if values.get(turnover_type) is True:
                return values
        raise ValidationError('Turnover type not found')

