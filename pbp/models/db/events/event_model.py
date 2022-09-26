from typing import List

from pydantic import conint, NonNegativeInt

from pbp.models.custom_base_model import CustomBaseModel
from pbp.models.db.stats_model import StatsModel


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
    event_stats: List[StatsModel] = []
    is_over_the_limit_event: bool
    is_second_chance_event: bool
    is_possession_ending_event: bool
    fouls_to_give: dict
    player_game_fouls: dict
    parent_event_id: str
    previous_event_id: str = None
    next_event_id: str = None

    @property
    def data(self):
        return self.dict(by_alias=True, exclude_none=True, exclude={'event_stats'})