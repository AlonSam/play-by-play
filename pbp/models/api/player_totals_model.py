from pydantic import Field

from pbp.models.api.api_base_model import APIBaseModel

two_pt_zones = ['at_rim', 'paint', 'left_corner_mid_range', 'left_wing_mid_range', 'center_mid_range',
                'right_wing_mid_range', 'right_corner_mid_range']
basic_two_pt_zones = ['at_rim', 'paint', 'mid_range']
three_pt_zones = ['right_corner_3', 'left_corner_3', 'right_wing_3', 'left_wing_3', 'center_3']
basic_three_pt_zones = ['corner_3', 'above_the_break_3']
all_zones = ['two_pt', 'three_pt', 'mid_range'] + two_pt_zones + three_pt_zones + basic_three_pt_zones


def get_makes_or_attempts(values, zone, string):
    return values.get(f'{zone}_{string}')


def get_assisted_unassisted(values, zone, string):
    return values.get(f'{string}_{zone}')


def to_camel(string: str) -> str:
    words = [word for word in string.split('_')]
    return ''.join([word.capitalize() for word in words])


class PlayerTotalsModel(APIBaseModel):
    player_id: str = None
    team_id: str = None
    name: str = None
    seconds_played: int = Field(default=0)
    seconds_played_off: int = Field(default=0)
    seconds_played_def: int = Field(default=0)
    games_played: int = Field(default=0)
    minutes_played: int = Field(default=0)
    plus_minus: int = Field(default=0)
    offensive_possessions: int = Field(default=0)
    defensive_possessions: int = Field(default=0)
    second_chance_offensive_possessions: int = Field(default=0)
    total_possessions: int = Field(default=0)
    at_rim_makes: int = Field(default=0)
    at_rim_attempts: int = Field(default=0)
    second_chance_at_rim_makes: int = Field(default=0)
    second_chance_at_rim_attempts: int = Field(default=0)
    paint_makes: int = Field(default=0)
    paint_attempts: int = Field(default=0)
    mid_range_makes: int = Field(default=0)
    mid_range_attempts: int = Field(default=0)
    left_corner_mid_range_makes: int = Field(default=0)
    left_corner_mid_range_attempts: int = Field(default=0)
    left_wing_mid_range_makes: int = Field(default=0)
    left_wing_mid_range_attempts: int = Field(default=0)
    center_mid_range_makes: int = Field(default=0)
    center_mid_range_attempts: int = Field(default=0)
    right_wing_mid_range_makes: int = Field(default=0)
    right_wing_mid_range_attempts: int = Field(default=0)
    right_corner_mid_range_makes: int = Field(default=0)
    right_corner_mid_range_attempts: int = Field(default=0)
    corner_3_makes: int = Field(default=0)
    corner_3_attempts: int = Field(default=0)
    right_corner_3_makes: int = Field(default=0)
    right_corner_3_attempts: int = Field(default=0)
    left_corner_3_makes: int = Field(default=0)
    left_corner_3_attempts: int = Field(default=0)
    second_chance_corner_3_makes: int = Field(default=0)
    second_chance_corner_3_attempts: int = Field(default=0)
    above_the_break_3_makes: int = Field(default=0)
    above_the_break_3_attempts: int = Field(default=0)
    right_wing_3_makes: int = Field(default=0)
    right_wing_3_attempts: int = Field(default=0)
    left_wing_3_makes: int = Field(default=0)
    left_wing_3_attempts: int = Field(default=0)
    center_3_makes: int = Field(default=0)
    center_3_attempts: int = Field(default=0)
    second_chance_above_the_break_3_makes: int = Field(default=0)
    second_chance_above_the_break_3_attempts: int = Field(default=0)
    two_pt_makes: int = Field(default=0)
    two_pt_attempts: int = Field(default=0)
    three_pt_makes: int = Field(default=0)
    three_pt_attempts: int = Field(default=0)
    free_throw_points: int = Field(default=0)
    points: int = Field(default=0)
    opponent_points: int = Field(default=0)
    second_chance_two_pt_makes: int = Field(default=0)
    second_chance_two_pt_attempts: int = Field(default=0)
    second_chance_three_pt_makes: int = Field(default=0)
    second_chance_three_pt_attempts: int = Field(default=0)
    second_chance_free_throw_points: int = Field(default=0)
    second_chance_points: int = Field(default=0)
    assisted_2_pts: int = Field(default=0)
    assisted_3_pts: int = Field(default=0)
    assisted_at_rim: int = Field(default=0)
    assisted_paint: int = Field(default=0)
    assisted_mid_range: int = Field(default=0)
    assisted_left_corner_mid_range: int = Field(default=0)
    assisted_left_wing_mid_range: int = Field(default=0)
    assisted_center_mid_range: int = Field(default=0)
    assisted_right_wing_mid_range: int = Field(default=0)
    assisted_right_corner_mid_range: int = Field(default=0)
    assisted_above_the_break_3: int = Field(default=0)
    assisted_left_wing_3: int = Field(default=0)
    assisted_right_wing_3: int = Field(default=0)
    assisted_center_3: int = Field(default=0)
    assisted_corner_3: int = Field(default=0)
    assisted_right_corner_3: int = Field(default=0)
    assisted_left_corner_3: int = Field(default=0)
    unassisted_two_pt: int = Field(default=0)
    unassisted_three_pt: int = Field(default=0)
    unassisted_at_rim: int = Field(default=0)
    unassisted_paint: int = Field(default=0)
    unassisted_mid_range: int = Field(default=0)
    unassisted_left_corner_mid_range: int = Field(default=0)
    unassisted_left_wing_mid_range: int = Field(default=0)
    unassisted_center_mid_range: int = Field(default=0)
    unassisted_right_wing_mid_range: int = Field(default=0)
    unassisted_right_corner_mid_range: int = Field(default=0)
    unassisted_above_the_break_3: int = Field(default=0)
    unassisted_left_wing_3: int = Field(default=0)
    unassisted_right_wing_3: int = Field(default=0)
    unassisted_center_3: int = Field(default=0)
    unassisted_corner_3: int = Field(default=0)
    unassisted_right_corner_3: int = Field(default=0)
    unassisted_left_corner_3: int = Field(default=0)
    putback_pts: int = Field(default=0)
    two_pt_attempts_blocked: int = Field(default=0)
    three_pt_attempts_blocked: int = Field(default=0)
    two_pt_assists: int = Field(default=0)
    three_pt_assists: int = Field(default=0)
    assists: int = Field(default=0)
    above_the_break_3_assists: int = Field(default=0)
    left_wing_3_assists: int = Field(default=0)
    right_wing_3_assists: int = Field(default=0)
    center_3_assists: int = Field(default=0)
    corner_3_assists: int = Field(default=0)
    left_corner_3_assists: int = Field(default=0)
    right_corner_3_assists: int = Field(default=0)
    at_rim_assists: int = Field(default=0)
    paint_assists: int = Field(default=0)
    mid_range_assists: int = Field(default=0)
    left_corner_mid_range_assists: int = Field(default=0)
    left_wing_mid_range_assists: int = Field(default=0)
    center_mid_range_assists: int = Field(default=0)
    right_wing_mid_range_assists: int = Field(default=0)
    right_corner_mid_range_assists: int = Field(default=0)
    assist_points: int = Field(default=0)
    off_two_pt_rebounds: int = Field(default=0)
    off_three_pt_rebounds: int = Field(default=0)
    off_free_throw_rebounds: int = Field(default=0)
    off_at_rim_rebounds: int = Field(default=0)
    off_paint_rebounds: int = Field(default=0)
    off_mid_range_rebounds: int = Field(default=0)
    off_corner_3_rebounds: int = Field(default=0)
    off_above_the_break_3_rebounds: int = Field(default=0)
    def_two_pt_rebounds: int = Field(default=0)
    def_three_pt_rebounds: int = Field(default=0)
    def_free_throw_rebounds: int = Field(default=0)
    def_at_rim_rebounds: int = Field(default=0)
    def_paint_rebounds: int = Field(default=0)
    def_mid_range_rebounds: int = Field(default=0)
    def_corner_3_rebounds: int = Field(default=0)
    def_above_the_break_3_rebounds: int = Field(default=0)
    def_rebounds: int = Field(default=0)
    off_rebounds: int = Field(default=0)
    off_two_pt_rebound_opportunities: int = Field(default=0)
    off_three_pt_rebound_opportunities: int = Field(default=0)
    off_free_throw_rebound_opportunities: int = Field(default=0)
    off_at_rim_rebound_opportunities: int = Field(default=0)
    off_paint_rebound_opportunities: int = Field(default=0)
    off_mid_range_rebound_opportunities: int = Field(default=0)
    off_corner_3_rebound_opportunities: int = Field(default=0)
    off_above_the_break_3_rebound_opportunities: int = Field(default=0)
    def_two_pt_rebound_opportunities: int = Field(default=0)
    def_three_pt_rebound_opportunities: int = Field(default=0)
    def_free_throw_rebound_opportunities: int = Field(default=0)
    def_at_rim_rebound_opportunities: int = Field(default=0)
    def_paint_rebound_opportunities: int = Field(default=0)
    def_mid_range_rebound_opportunities: int = Field(default=0)
    def_corner_3_rebound_opportunities: int = Field(default=0)
    def_above_the_break_3_rebound_opportunities: int = Field(default=0)
    def_rebound_opportunities: int = Field(default=0)
    off_rebound_opportunities: int = Field(default=0)
    rebounds: int = Field(default=0)
    self_off_rebounds: int = Field(default=0)
    self_off_rebound_opportunities: int = Field(default=0)
    deflections: int = Field(default=0)
    steals: int = Field(default=0)
    bad_pass_steals: int = Field(default=0)
    ball_handling_steals: int = Field(default=0)
    other_steals: int = Field(default=0)
    live_ball_turnovers: int = Field(default=0)
    bad_pass_turnovers: int = Field(default=0)
    ball_handling_turnovers: int = Field(default=0)
    travel_turnovers: int = Field(default=0)
    backcourt_violation_turnovers: int = Field(default=0)
    double_dribble_turnovers: int = Field(default=0)
    three_second_violation_turnovers: int = Field(default=0)
    five_second_violation_turnovers: int = Field(default=0)
    eight_second_violation_turnovers: int = Field(default=0)
    shot_clock_violation_turnovers: int = Field(default=0)
    out_of_bounds_turnovers: int = Field(default=0)
    other_turnovers: int = Field(default=0)
    turnovers: int = Field(default=0)
    second_chance_turnovers: int = Field(default=0)
    shooting_fouls: int = Field(default=0)
    fouls: int = Field(default=0)
    offensive_fouls: int = Field(default=0)
    fouls_drawn: int = Field(default=0)
    shooting_fouls_drawn: int = Field(default=0)
    offensive_fouls_drawn: int = Field(default=0)
    free_throw_makes: int = Field(default=0)
    free_throw_attempts: int = Field(default=0)
    two_pt_and_one_trips: int = Field(default=0)
    three_pt_and_one_trips: int = Field(default=0)
    technical_ft_trips: int = Field(default=0)
    two_pt_shooting_fouls_drawn: int = Field(default=0)
    three_pt_shooting_fouls_drawn: int = Field(default=0)
    non_shooting_fouls_drawn: int = Field(default=0)
    blocked_2s: int = Field(default=0)
    blocked_3s: int = Field(default=0)
    blocked_at_rim: int = Field(default=0)
    blocked: int = Field(default=0)
    blocks: int = Field(default=0)
    at_rim_blocks: int = Field(default=0)
    paint_blocks: int = Field(default=0)
    mid_range_blocks: int = Field(default=0)
    corner_3_blocks: int = Field(default=0)
    above_the_break_3_blocks: int = Field(default=0)
    offensive_rating: float = Field(default=0.0)
    defensive_rating: float = Field(default=0.0)
    assisted_two_pt_pct: float = Field(default=0.0)
    assisted_three_pt_pct: float = Field(default=0.0)
    three_pt_pct: float = Field(default=0.0)
    second_chance_three_pt_pct: float = Field(default=0.0)
    two_pt_pct: float = Field(default=0.0)
    second_chance_two_pt_pct: float = Field(default=0.0)
    ts_pct: float = Field(default=0.0)
    second_chance_ts_pct: float = Field(default=0.0)
    efg_pct: float = Field(default=0.0)
    second_chance_efg_pct: float = Field(default=0.0)
    three_pt_frequency: float = Field(default=0.0)
    three_pt_pct_blocked: float = Field(default=0.0)
    two_pt_pct_blocked: float = Field(default=0.0)
    at_rim_pct_blocked: float = Field(default=0.0)
    usage: float = Field(default=0.0)
    live_ball_turnovers_pct: float = Field(default=0.0)
    def_ft_rebound_pct: float = Field(default=0.0)
    def_two_pt_rebound_pct: float = Field(default=0.0)
    def_three_pt_rebound_pct: float = Field(default=0.0)
    off_ft_rebound_pct: float = Field(default=0.0)
    off_two_pt_rebound_pct: float = Field(default=0.0)
    off_three_pt_rebound_pct: float = Field(default=0.0)
    def_rebound_pct: float = Field(default=0.0)
    off_rebound_pct: float = Field(default=0.0)
    off_at_rim_rebound_pct: float = Field(default=0.0)
    off_paint_rebound_pct: float = Field(default=0.0)
    off_mid_range_rebound_pct: float = Field(default=0.0)
    off_corner_3_rebound_pct: float = Field(default=0.0)
    off_above_the_break_3_rebound_pct: float = Field(default=0.0)
    def_at_rim_rebound_pct: float = Field(default=0.0)
    def_paint_rebound_pct: float = Field(default=0.0)
    def_mid_range_rebound_pct: float = Field(default=0.0)
    def_corner_3_rebound_pct: float = Field(default=0.0)
    def_above_the_break_3_rebound_pct: float = Field(default=0.0)
    self_offensive_rebounds_pct: float = Field(default=0.0)
    at_rim_frequency: float = Field(default=0.0)
    at_rim_accuracy: float = Field(default=0.0)
    assisted_at_rim_pct: float = Field(default=0.0)
    paint_frequency: float = Field(default=0.0)
    paint_accuracy: float = Field(default=0.0)
    assisted_paint_pct: float = Field(default=0.0)
    mid_range_frequency: float = Field(default=0.0)
    mid_range_accuracy: float = Field(default=0.0)
    assisted_mid_range_pct: float = Field(default=0.0)
    left_corner_mid_range_frequency: float = Field(default=0.0)
    left_corner_mid_range_accuracy: float = Field(default=0.0)
    assisted_left_corner_mid_range_pct: float = Field(default=0.0)
    left_wing_mid_range_frequency: float = Field(default=0.0)
    left_wing_mid_range_accuracy: float = Field(default=0.0)
    assisted_left_wing_mid_range_pct: float = Field(default=0.0)
    center_mid_range_frequency: float = Field(default=0.0)
    center_mid_range_accuracy: float = Field(default=0.0)
    assisted_center_mid_range_pct: float = Field(default=0.0)
    right_wing_mid_range_frequency: float = Field(default=0.0)
    right_wing_mid_range_accuracy: float = Field(default=0.0)
    assisted_right_wing_mid_range_pct: float = Field(default=0.0)
    right_corner_mid_range_frequency: float = Field(default=0.0)
    right_corner_mid_range_accuracy: float = Field(default=0.0)
    assisted_right_corner_mid_range_pct: float = Field(default=0.0)
    corner_3_frequency: float = Field(default=0.0)
    corner_3_accuracy: float = Field(default=0.0)
    assisted_corner_3_pct: float = Field(default=0.0)
    left_corner_3_frequency: float = Field(default=0.0)
    left_corner_3_accuracy: float = Field(default=0.0)
    assisted_left_corner_3_pct: float = Field(default=0.0)
    right_corner_3_frequency: float = Field(default=0.0)
    right_corner_3_accuracy: float = Field(default=0.0)
    assisted_right_corner_3_pct: float = Field(default=0.0)
    above_the_break_3_frequency: float = Field(default=0.0)
    above_the_break_3_accuracy: float = Field(default=0.0)
    assisted_above_the_break_3_pct: float = Field(default=0.0)
    right_wing_3_frequency: float = Field(default=0.0)
    right_wing_3_accuracy: float = Field(default=0.0)
    assisted_right_wing_3_pct: float = Field(default=0.0)
    left_wing_3_frequency: float = Field(default=0.0)
    left_wing_3_accuracy: float = Field(default=0.0)
    assisted_left_wing_3_pct: float = Field(default=0.0)
    second_chance_at_rim_frequency: float = Field(default=0.0)
    second_chance_at_rim_accuracy: float = Field(default=0.0)
    assisted_second_chance_at_rim_pct: float = Field(default=0.0)
    second_chance_corner_3_frequency: float = Field(default=0.0)
    second_chance_corner_3_accuracy: float = Field(default=0.0)
    assisted_second_chance_corner_3_pct: float = Field(default=0.0)
    second_chance_above_the_break_3_frequency: float = Field(default=0.0)
    second_chance_above_the_break_3_accuracy: float = Field(default=0.0)
    assisted_second_chance_above_the_break_3_pct: float = Field(default=0.0)
    shooting_fouls_drawn_pct: float = Field(default=0.0)
    avg_2pt_shot_distance: float = Field(default=0.0)
    avg_3pt_shot_distance: float = Field(default=0.0)

    class Config:
        alias_generator = to_camel

#     @root_validator
#     def make_aggregations(cls, values: Dict) -> Dict:
#         values['seconds_played'] = values.get('seconds_played_off') + values.get('seconds_played_def')
#         values.update(cls._make_shot_aggregations(values))
#         values.update(cls._calculate_shooting_percentages(values))
#         values.update(cls._make_rebound_aggregations(values))
#         return values
#
#     @staticmethod
#     def _make_rebound_aggregations(values: Dict) -> Dict:
#         prefixes = ['off', 'def']
#         suffixes = ['rebounds', 'rebound_opportunities']
#         for prefix in prefixes:
#             for suffix in suffixes:
#                 values[f'{prefix}_two_pt_{suffix}'] = sum(
#                     [values.get(f'{prefix}_{zone}_{suffix}') for zone in basic_two_pt_zones])
#                 values[f'{prefix}_three_pt_{suffix}'] = sum(
#                     [values.get(f'{prefix}_{zone}_{suffix}') for zone in basic_three_pt_zones])
#                 values[f'{prefix}_{suffix}'] = values.get(f'{prefix}_two_pt_{suffix}') + \
#                                                       values.get(f'{prefix}_three_pt_{suffix}') + \
#                                                       values.get(f'{prefix}_free_throw_{suffix}')
#         return values
#
#     @staticmethod
#     def _make_shot_aggregations(values: Dict) -> Dict:
#         for zone in two_pt_zones:
#             values[f'{zone}_makes'] = values.get(f'assisted_{zone}') + values.get(f'unassisted_{zone}')
#         for zone in three_pt_zones:
#             values[f'{zone}_makes'] = values.get(f'assisted_{zone}') + values.get(f'unassisted_{zone}')
#         prefixes = ['', 'second_chance_']
#         suffixes = ['makes', 'attempts']
#         for prefix in prefixes:
#             for suffix in suffixes:
#                 values[f'{prefix}two_pt_{suffix}'] = sum(
#                     [get_makes_or_attempts(values, zone, suffix) for zone in two_pt_zones])
#                 values[f'{prefix}three_pt_{suffix}'] = sum(
#                     [get_makes_or_attempts(values, zone, suffix) for zone in three_pt_zones])
#                 values[f'{prefix}mid_range_{suffix}'] = sum(
#                     [get_makes_or_attempts(values, zone, suffix) for zone in two_pt_zones[2:]])
#                 values[f'{prefix}corner_3_{suffix}'] = sum(
#                     [get_makes_or_attempts(values, zone, suffix) for zone in three_pt_zones[:2]])
#                 values[f'{prefix}above_the_break_3_{suffix}'] = sum(
#                     [get_makes_or_attempts(values, zone, suffix) for zone in three_pt_zones[2:]])
#         suffixes = ['assisted', 'unassisted']
#         for suffix in suffixes:
#             values[f'{suffix}_2_pts'] = sum(
#                 [get_assisted_unassisted(values, zone, suffix) * 2 for zone in two_pt_zones])
#             values[f'{suffix}_3_pts'] = sum(
#                 [get_assisted_unassisted(values, zone, suffix) * 3 for zone in three_pt_zones])
#             values[f'{suffix}_mid_range'] = sum(
#                 [get_assisted_unassisted(values, zone, suffix) for zone in two_pt_zones[2:]])
#             values[f'{suffix}_corner_3'] = sum(
#                 [get_assisted_unassisted(values, zone, suffix) for zone in three_pt_zones[:2]])
#             values[f'{suffix}_above_the_break_3'] = sum(
#                 [get_assisted_unassisted(values, zone, suffix) for zone in three_pt_zones[2:]])
#         return values
#
#     @staticmethod
#     def _calculate_shooting_percentages(values: Dict) -> Dict:
#         for zone in all_zones:
#             success_num = values.get(f'{zone}_makes')
#             attempts = values.get(f'{zone}_attempts')
#             values[f'{zone}_accuracy'] = calculate_percentages(success_num, attempts)
#             if zone in two_pt_zones or zone in basic_two_pt_zones:
#                 zone_attempts = values.get('two_pt_attempts')
#             else:
#                 zone_attempts = values.get('three_pt_attempts')
#             values[f'{zone}_frequency'] = calculate_percentages(attempts, zone_attempts)
#         return values
#
#
# def calculate_percentages(success_num: int, attempts: int) -> float:
#     if attempts == 0:
#         return 0.0
#     return round(success_num / attempts, 2)
