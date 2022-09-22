from __future__ import annotations

from pydantic import Field

from .api_base_model import APIBaseModel


class PossessionAPIModel(APIBaseModel):
    possession_id: str
    game_id: str
    events: str
    period: int
    start_time: str
    end_time: str
    duration: int
    margin: int
    score: dict
    team: str
    opponent: str
    offense_lineup: str
    defense_lineup: str
    start_type: str
    fg_2m: int = Field(default=0, alias='FG2M')
    fg_2a: int = Field(default=0, alias='FG2A')
    fg_3m: int = Field(default=0, alias='FG3M')
    fg_3a: int = Field(default=0, alias='FG3A')
    ftm: int = Field(default=0, alias='FTM')
    fta: int = Field(default=0, alias='FTA')
    turnovers: int = Field(default=0)
    offensive_rebounds: int = Field(default=0)


    @property
    def data(self):
        return self.dict(by_alias=True, exclude_none=True)