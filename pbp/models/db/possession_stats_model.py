from enum import Enum

from pydantic import Field

from models import CustomBaseModel


class Instance(str, Enum):
    player = "player"
    team = "team"
    lineup = "lineup"


class PossessionStatsModel(CustomBaseModel):
    possession_id: str
    instance: Instance
    player_id: str = None
    team_id: str = None
    lineup_id: str = None
    seconds_played_off: int = Field(default=0)
    seconds_played_def: int = Field(default=0)
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