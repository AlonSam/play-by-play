from typing import List, Dict

from pydantic import Field

from pbp.models.boxscore_model import BoxScoreModel
from pbp.models.custom_base_model import CustomBaseModel
from pbp.models.details_model import DetailsModel


class GameModel(CustomBaseModel):
    game_id: str = Field(alias='_id')
    basket_id: str
    details: DetailsModel
    boxscore: List[BoxScoreModel]
    possessions: List[str]

    class Config:
        arbitrary_types_allowed = True

    @property
    def data(self) -> Dict:
        return self.dict(by_alias=True)
