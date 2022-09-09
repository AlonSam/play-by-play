from .event import Event


class TurnoverEvent(Event):
    is_steal: bool
    steal_player_id: str = None
    is_3_second_violation: bool
    is_5_second_violation: bool
    is_8_second_violation: bool
    is_backcourt_violation: bool
    is_bad_pass: bool
    is_ball_handling: bool
    is_double_dribble: bool
    is_lane_violation: bool
    is_offensive_foul: bool
    is_out_of_bounds: bool
    is_shot_clock_violation: bool
    is_travel: bool
    is_unknown: bool
