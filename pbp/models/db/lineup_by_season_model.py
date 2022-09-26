from typing import List, Dict

from pydantic import Field

from pbp.models.custom_base_model import CustomBaseModel


class LineupModel(CustomBaseModel):
    id: str = Field(alias='_id')
    team_id: str
    season: str
    games: List[str] = list()
    possessions: Dict[str, List[str]] = dict()

    @property
    def data(self):
        return self.dict(by_alias=True, exclude_none=True)