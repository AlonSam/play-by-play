from typing import List

from pydantic import Field, NonNegativeInt

from .custom_base_model import CustomBaseModel
from .events.event_model import EventModel


class PossessionModel(CustomBaseModel):
    possession_id: str = Field(alias='_id')
    game_id: str
    events: List[EventModel]
    period: int
    start_time: str
    end_time: str
    duration: NonNegativeInt
    margin: int
    score: dict
    offense_team_id: str
    defense_team_id: str
    offense_lineup_id: str
    defense_lineup_id: str
    previous_possession_id: str = None
    next_possession_id: str = None
    possession_start_type: str
    is_over_the_limit: bool
    previous_possession_ending_event_id: str = None
    previous_possession_end_shooter_player_id: str = None
    previous_possession_end_rebound_player_id: str = None
    previous_possession_end_steal_player_id: str = None