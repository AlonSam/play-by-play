from typing import List

from models import CustomBaseModel


class PhaseModel(CustomBaseModel):
    regular_season: List[str]
    quarter_finals: List[str]
    semi_finals: List[str]
    finals: List[str]
    winner_cup: List[str]


class SeasonModel(CustomBaseModel):
    season: str
    games: PhaseModel

    @property
    def data(self):
        return self.dict(by_alias=True, exclude_none=True)