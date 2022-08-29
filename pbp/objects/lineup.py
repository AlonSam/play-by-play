from typing import Optional, List

from pydantic import validator

from pbp.objects.my_base_model import MyBaseModel


class Lineup(MyBaseModel):
    """
    TODO
    """
    id: str
    team_id: int
    player_ids: Optional[List[int]]

    @validator('player_ids', always=True)
    def validate_player_ids(cls, value, values):
        players = [int(player) for player in values.get('id').split('-')]
        if len(players) != 5:
            raise ValueError('Lineup must include exactly 5 players')
        return players
