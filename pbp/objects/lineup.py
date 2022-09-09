from typing import List, Dict

from pydantic import validator, Field

from pbp.objects.my_base_model import MyBaseModel


class Lineup(MyBaseModel):
    """
    TODO
    """
    id: str = Field(alias='_id')
    team_id: str
    player_ids: List[str] = None
    games: List[str] = list()
    possessions: Dict[str, List[str]] = dict()

    @validator('player_ids', always=True)
    def validate_player_ids(cls, value, values):
        if value is not None:
            return value
        players = [player for player in values.get('id').split('-')]
        if len(players) != 5:
            raise ValueError('Lineup must include exactly 5 players')
        return players

    @property
    def data(self) -> Dict:
        return self.dict(by_alias=True)