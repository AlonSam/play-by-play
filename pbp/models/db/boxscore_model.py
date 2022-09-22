from models.custom_base_model import CustomBaseModel


class BoxScoreModel(CustomBaseModel):
    """
    Class for boxscore items from Segev Sports
    """
    player_id: str
    team_id: str
    game_id: str
    points: int
    minutes: str = None
    starter: bool = None
    FGM: int
    FGA: int
    FGPCT: float
    FG2M: int
    FG2A: int
    FG2PCT: float
    FG3M: int
    FG3A: int
    FG3PCT: float
    FTM: int
    FTA: int
    FTPCT: float
    defensive_rebounds: int
    offensive_rebounds: int
    total_rebounds: int
    assists: int
    turnovers: int
    steals: int
    blocks: int
    blocked: int
    fouls: int
    fouls_drawn: int
    fastbreak_points: int
    second_chance_points: int
    dunks: int
    deflections: int = None
    recoveries: int = None
    vps: float = None
    plus_minus: int = None
    pir: int

    @property
    def data(self):
        return self.dict(by_alias=True, exclude_none=True)

