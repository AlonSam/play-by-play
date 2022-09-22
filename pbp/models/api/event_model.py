from .api_base_model import APIBaseModel


class EventAPIModel(APIBaseModel):
    event_id: str
    game_id: str
    team_id: str
    team_name: str
    offense_team_id: str
    offense_team_name: str
    player_id: str
    player_name: str
    lineups: dict
    lineup_ids: dict
    action_type: str
    sub_type: str = None
    period: int
    time: str
    seconds_remaining: int
    score: dict
    margin: int
    is_penalty_event: bool
    is_second_chance_event: bool
    parent_event_id: str
    previous_event_id: str = None
    next_event_id: str = None
