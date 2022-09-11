from pydantic import conint, NonNegativeInt

from ..custom_base_model import CustomBaseModel


class EventModel(CustomBaseModel):
    event_id: str
    game_id: str
    team_id: str
    offense_team_id: str
    player_id: str
    lineup_ids: dict
    action_type: str
    sub_type: str
    period: int
    time: str
    seconds_remaining: conint(ge=0, le=600)
    seconds_since_previous_event: NonNegativeInt
    score: dict
    margin: int
    is_penalty_event: bool
    is_second_chance_event: bool
    is_possession_ending_event: bool
    fouls_to_give: dict
    player_game_fouls: dict
    parent_event_id: str
    previous_event_id: str = None
    next_event_id: str = None
