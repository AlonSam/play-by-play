from enum import Enum


class Phase(str, Enum):
    regular_season = "Regular Season"
    playoffs = "Playoffs"
    pre_season = 'Winner Cup'
    all = "All"


class League(str, Enum):
    winner_league = 'Winner League'


class Instance(str, Enum):
    player = 'player'
    team = 'team'
    lineup = 'lineup'