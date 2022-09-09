import datetime
from typing import List

from pbp.objects.my_base_model import MyBaseModel


class SegevDetailsItem(MyBaseModel):
    """
    class for game data from Segev Sports

    :param dict item: dict with game data
    """
    game_id: str
    basket_id: str
    competition: str
    season: str
    phase: str
    round: int
    home_team: str
    away_team: str
    home_id: str
    away_id: str
    home_score: int
    away_score: int
    attendance: int
    referees: List[str]
    observer: str
    time: datetime.datetime
    final: bool
