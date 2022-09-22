import datetime

from .api_base_model import APIBaseModel


class GameAPIModel(APIBaseModel):
    game_id: str
    basket_id: str
    date: datetime.date
    home_team_id: str
    away_team_id: str
    home_team_name: str
    away_team_name: str
    home_score: int
    away_score: int
    home_possessions: int
    away_possessions: int

    class Config:
        schema_extra = {
            "example": {
                "gameId": "35347",
                "basketId": "24495",
                "date": "2021-10-23",
                "homeTeamId": "2",
                "awayTeamId": "4",
                "homeTeamName": "Maccabi Tel Aviv",
                "awayTeamName": "Hapoel Jerusalem",
                "homeScore": 104,
                "awayScore": 80,
                "homePossessions": 77,
                "awayPossessions": 77
            }
        }
