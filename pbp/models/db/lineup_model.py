from typing import Dict, Set

from pydantic import validator, Field

from pbp.models.custom_base_model import CustomBaseModel


class LineupModel(CustomBaseModel):
    id: str = Field(alias='_id')
    team_id: str
    season: str
    player_ids: Set[str] = None
    games: Set[str] = set()
    possessions: Dict[str, Set[str]] = dict()

    @validator('player_ids', always=True)
    def validate_player_ids(cls, value, values) -> Set[str]:
        if value is not None:
            return value
        players = {player for player in values.get('id').split('-')}
        if len(players) != 5:
            raise ValueError('Lineup must include exactly 5 players')
        return players

    @property
    def data(self):
        data = self.dict(by_alias=True, exclude_none=True)
        data['games'] = list(data['games'])
        data['playerIds'] = list(data['playerIds'])
        for key, value in data['possessions'].items():
            data['possessions'][key] = list(data['possessions'][key])
        return data