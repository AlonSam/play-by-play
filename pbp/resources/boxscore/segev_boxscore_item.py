from typing import Optional

from pydantic import BaseModel


class Shot(BaseModel):
    made: int
    attempted: int
    pct: float


class Rebound(BaseModel):
    treb: int
    dreb: int
    oreb: int


class Foul(BaseModel):
    made: int
    drawn: int


class Block(BaseModel):
    made: int
    blocked: int


class SegevBoxScoreItem(BaseModel):
    """
    Class for boxscore items from Segev Sports
    """
    player_id: int
    team_id: int
    game_id: int
    pts: int
    min: Optional[str]
    starter: Optional[bool]
    fg: Shot
    two_pt: Shot
    three_pt: Shot
    ft: Shot
    reb: Rebound
    ast: int
    to: int
    stl: int
    blocks: Block
    fouls: Foul
    fbpts: int
    scpts: int
    dunk: int
    pm: Optional[int]
    pir: int


