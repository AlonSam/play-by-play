import datetime
from typing import List

from pbp.models.custom_base_model import CustomBaseModel


class DetailsModel(CustomBaseModel):
    game_id: str
    basket_id: str
    competition: str
    season: str
    phase: str
    round: int
    home_team: str
    away_team: str
    home_id: str
    away_id: str
    home_score: int
    away_score: int
    attendance: int
    referees: List
    observer: str
    time: datetime.datetime
    final: bool

    @property
    def data(self):
        return self.dict(by_alias=True)