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
    player_id: str
    team_id: str
    game_id: str
    pts: int
    min: str = None
    starter: bool = None
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
    pm: int = None
    pir: int

    @property
    def data(self):
        return self.dict(by_alias=True, exclude_none=True)


