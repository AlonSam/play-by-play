from typing import List, Union

from pydantic import Field, NonNegativeInt

from pbp.models.custom_base_model import CustomBaseModel
from pbp.models.db.events import *
from pbp.models.db.stats_model import StatsModel


class PossessionModel(CustomBaseModel):
    possession_id: str = Field(alias='_id')
    game_id: str
    events: List[Union[FieldGoalEventModel, SubstitutionEventModel, FreeThrowEventModel, ReboundEventModel,
                       TurnoverEventModel, FoulEventModel, TimeoutEventModel, DeflectionEventModel,
                       EndOfPeriodEventModel, StartOfPeriodEventModel]]
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
    possession_stats: List[StatsModel]
    previous_possession_ending_event_id: str = None
    previous_possession_end_shooter_player_id: str = None
    previous_possession_end_rebound_player_id: str = None
    previous_possession_end_steal_player_id: str = None

    @property
    def data(self):
        events = [event.data for event in self.events]
        data = self.dict(by_alias=True, exclude_none=True, exclude={'events'})
        data['events'] = events
        return data