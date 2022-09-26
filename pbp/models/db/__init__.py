from pbp.models.db.boxscore_model import BoxScoreModel
from pbp.models.db.details_model import DetailsModel
from pbp.models.db.events import *
from pbp.models.db.game_model import GameModel
from pbp.models.db.lineup_model import LineupModel
from pbp.models.db.player_model import PlayerModel
from pbp.models.db.possession_model import PossessionModel
from pbp.models.db.team_model import TeamModel

__all__ = [
    "PossessionModel",
    "TeamModel",
    "PlayerModel",
    "LineupModel",
    "GameModel",
    "DetailsModel",
    "BoxScoreModel",
    "EventModel",
    "FoulEventModel",
    "FieldGoalEventModel",
    "FreeThrowEventModel",
    "DeflectionEventModel",
    "TurnoverEventModel",
    "TimeoutEventModel",
    "ReboundEventModel",
    "EndOfPeriodEventModel",
    "SubstitutionEventModel",
    "StartOfPeriodEventModel"
]


def to_camel(string: str) -> str:
    words = [word for word in string.split('_')]
    return ''.join([word.capitalize() if words.index(word) != 0 else word for word in words])