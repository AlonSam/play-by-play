from pbp.models.custom_base_model import CustomBaseModel


class Shot(CustomBaseModel):
    made: int
    attempted: int
    pct: float


class Rebound(CustomBaseModel):
    treb: int
    dreb: int
    oreb: int


class Foul(CustomBaseModel):
    made: int
    drawn: int


class Block(CustomBaseModel):
    made: int
    blocked: int


class BoxScoreModel(CustomBaseModel):
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
    fastbreak_pts: int
    second_chance_pts: int
    dunk: int
    dfl: int = None
    rec: int = None
    vps: float = None
    plus_minus: int = None
    pir: int

    @property
    def data(self):
        return self.dict(by_alias=True, exclude_none=True)


