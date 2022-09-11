from typing import List, Dict

from pydantic import Field

from pbp.models.boxscore_model import BoxScoreModel
from pbp.models.custom_base_model import CustomBaseModel


class TeamModel(CustomBaseModel):
    """
    TODO
    """
    id: str = Field(alias='_id')
    name: str
    games: List[str] = list()
    possessions: Dict[str, List[str]] = dict()
    boxscores: List[BoxScoreModel] = list()

    @property
    def data(self) -> Dict:
        return self.dict(by_alias=True)
