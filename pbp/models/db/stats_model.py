from typing import Union

from pbp.models import CustomBaseModel


class StatsModel(CustomBaseModel):
    player_id: str
    team_id: str
    stat_key: str
    stat_value: Union[int, float]
    opponent_team_id: str = None
    lineup_id: str = None
    opponent_lineup_id: str = None