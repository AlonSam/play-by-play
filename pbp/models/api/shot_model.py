from pbp.models.api.api_base_model import APIBaseModel


class ShotModel(APIBaseModel):
    event_id: str
    player_id: str
    team_id: str
    opponent_team_id: str
    lineup_id: str
    opponent_lineup_id: str
    made: bool
    x: float
    y: float
    time: int
    shot_value: int
    is_putback: bool
    basic_shot_zone: str
    shot_zone: str
    margin: int
    is_and_one: bool
    is_assisted: bool
    assist_player_id: str = None
    is_blocked: bool
    block_player_id: str = None

    class Config:
        schema_extra = {
            "example": {
                "eventId": "353700435",
                "playerId": "2031",
                "teamId": "2",
                "opponentTeamId": "10",
                "lineupId": "1415-1419-2031-82-847",
                "opponentLineupId": "128-1623-408-46-6906",
                "made": True,
                "x": 468.53,
                "y": 195.8852,
                "time": 437,
                "shotValue": 3,
                "isPutback": False,
                "basicShotZone": "AboveTheBreak3",
                "shotZone": "LeftWing3",
                "margin": 4,
                "isAndOne": False,
                "isAssisted": True,
                "assistPlayerId": "847",
                "isBlocked": False,
                "blockPlayerId": None
            }
        }
