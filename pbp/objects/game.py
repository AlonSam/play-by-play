from typing import List, Dict

from pydantic import Field

from pbp.objects.my_base_model import MyBaseModel
from pbp.resources.boxscore.segev_boxscore_item import SegevBoxScoreItem
from pbp.resources.details.segev_details_item import SegevDetailsItem


class Game(MyBaseModel):
    game_id: str = Field(alias='_id')
    basket_id: str
    details: SegevDetailsItem
    boxscore: List[SegevBoxScoreItem]
    possessions: List[str]

    @property
    def data(self) -> Dict:
        return self.dict(by_alias=True)
