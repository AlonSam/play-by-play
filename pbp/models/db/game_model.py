from typing import List

from pydantic import Field

from pbp.models.custom_base_model import CustomBaseModel
from pbp.models.db import BoxScoreModel
from pbp.models.db import DetailsModel


class GameModel(CustomBaseModel):
    id: str = Field(alias='_id')
    basket_id: str
    details: DetailsModel
    boxscore: List[BoxScoreModel]
    possessions: List[str]

    class Config:
        arbitrary_types_allowed = True

    @property
    def data(self):
        return self.dict(by_alias=True, exclude_none=True)