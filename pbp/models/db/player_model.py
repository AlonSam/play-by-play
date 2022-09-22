from typing import Dict, List

from pydantic import Field

from models.custom_base_model import CustomBaseModel
from models.db import BoxScoreModel


class PlayerModel(CustomBaseModel):
    """
    TODO
    """
    id: str = Field(alias='_id')
    team_id: str
    team_ids: Dict[str, str] = dict()
    name: str
    hebrew_name: str
    shirt_number: str
    games: List[str] = list()
    possessions: Dict[str, List[str]] = dict()
    boxscores: List[BoxScoreModel] = list()

    @property
    def data(self):
        return self.dict(by_alias=True, exclude_none=True)