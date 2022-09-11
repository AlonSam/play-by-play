from typing import List, Dict

from pydantic import Field

from pbp.models.boxscore_model import BoxScoreModel
from pbp.models.custom_base_model import CustomBaseModel


class PlayerModel(CustomBaseModel):
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
    boxscores: List[BoxScoreModel] = list()

    @property
    def data(self) -> Dict:
        return self.dict(by_alias=True)