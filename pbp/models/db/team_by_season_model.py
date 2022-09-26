from __future__ import annotations

from typing import List, Dict, Set

from pbp.models.custom_base_model import CustomBaseModel
from pbp.models.db import BoxScoreModel


class TeamBySeasonModel(CustomBaseModel):
    """
    TODO
    """
    team_id: str
    season: str
    games: Set[str] = set()
    possessions: Dict[str, Set[str]] = {}
    boxscores: List[BoxScoreModel] = list()

    @property
    def data(self):
        data = self.dict(by_alias=True, exclude_none=True)
        data['games'] = list(data['games'])
        for key, value in data['possessions'].items():
            data['possessions'][key] = list(data['possessions'][key])
        return data