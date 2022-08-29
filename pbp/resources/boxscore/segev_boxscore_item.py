from typing import Optional

from pbp.objects.my_base_model import MyBaseModel


class Shot(MyBaseModel):
    made: int
    attempted: int
    pct: float


class Rebound(MyBaseModel):
    treb: int
    dreb: int
    oreb: int


class Foul(MyBaseModel):
    made: int
    drawn: int


class Block(MyBaseModel):
    made: int
    blocked: int


class SegevBoxScoreItem(MyBaseModel):
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


