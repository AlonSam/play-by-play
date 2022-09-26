from typing import Dict, List, Set

from pbp.models.custom_base_model import CustomBaseModel
from pbp.models.db import BoxScoreModel


class PlayerBySeasonModel(CustomBaseModel):
    """
    TODO
    """
    player_id: str
    team_id: str
    season: str
    games: Set[str] = set()
    possessions: Dict[str, Set[str]] = dict()
    events: Set[str] = set()
    boxscores: List[BoxScoreModel] = list()

    @property
    def data(self):
        data = self.dict(by_alias=True, exclude_none=True)
        data['games'] = list(data['games'])
        data['events'] = list(data['events'])
        for key, value in data['possessions'].items():
            data['possessions'][key] = list(data['possessions'][key])
        return data