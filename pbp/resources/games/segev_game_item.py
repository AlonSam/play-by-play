import datetime
from typing import List

from pbp.objects.my_base_model import MyBaseModel


class SegevGameItem(MyBaseModel):
    """
    class for game data from Segev Sports

    :param dict item: dict with game data
    """
    game_id: int
    basket_id: int
    competition: str
    season: str
    phase: str
    round: int
    home_team: str
    away_team: str
    home_id: int
    away_id: int
    home_score: int
    away_score: int
    attendance: int
    referees: List[str]
    observer: str
    time: datetime.datetime
    final: bool
