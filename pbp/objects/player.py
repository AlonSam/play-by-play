from typing import List, Dict

from pydantic import Field

from pbp.objects.my_base_model import MyBaseModel
from pbp.resources.boxscore.segev_boxscore_item import SegevBoxScoreItem


class Player(MyBaseModel):
    """
    TODO
    """
    id: str = Field(alias='_id')
    team_id: str
    name: str
    hebrew_name: str
    shirt_number: str
    games: List[str] = list()
    possessions: Dict[str, List[str]] = dict()
    boxscores: List[SegevBoxScoreItem] = list()

    @property
    def data(self) -> Dict:
        return self.dict(by_alias=True)