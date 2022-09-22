KEY_ATTR_MAPPER = {
    "playerId": "player_id",
    "jerseyNumber": "shirt_num",
    "plusMinus": "plus_minus",
    "fb": "fastbreak_points",
    "rate": "pir",
    "sc": "second_chance_points",
    "Points_from_turnovers": "turnover_points",
    "Points_in_the_paint": "points_in_the_paint",
    "Second_chance_points": "second_chance_points",
    'ast': 'assists',
    'to': 'turnovers',
    'blk': 'blocks',
    'blk_against': 'blocked',
    'f': 'fouls',
    'f_drawn': 'fouls_drawn',
    'stl': 'steals',
    'dunk': 'dunks',
    'dfl': 'deflections',
    'rec': 'recoveries',
    'reb_o': 'offensive_rebounds',
    'reb_d': 'defensive_rebounds',
    'fg_3m': 'FG3M',
    'fg_2m': 'FG2M',
    'ft_m': 'FTM'
    }

KEYS = ['team_id', 'game_id', 'vps', 'points', 'starter', 'minutes']


class SegevBoxScoreItem:
    """
    Class for boxscore items from Segev Sports
    """
    def __init__(self, data):
        for key, value in KEY_ATTR_MAPPER.items():
            if data.get(key) is not None:
                setattr(self, value, str(data.get(key)))
        for key in KEYS:
            if data.get(key) is not None:
                setattr(self, key, data.get(key))
        self._set_attributes(data)

    def _set_attributes(self, data):
        data = {k: int(v) if isinstance(v, str) and v.isnumeric() else v for k, v in data.items()}
        self.total_rebounds = int(self.offensive_rebounds) + int(self.defensive_rebounds)
        self.FG3A = int(self.FG3M) + data['fg_3mis']
        self.FG2A = int(self.FG2M) + data['fg_2mis']
        self.FTA = int(self.FTM) + data['ft_mis']
        self.FGM = int(self.FG2M) + int(self.FG3M)
        self.FGA = int(self.FG2A) + int(self.FG3A)
        self.FG2PCT = self.cal_pct(int(self.FG2M), int(self.FG2A))
        self.FG3PCT = self.cal_pct(int(self.FG3M), int(self.FG3A))
        self.FGPCT = self.cal_pct(int(self.FGM), int(self.FGA))
        self.FTPCT = self.cal_pct(int(self.FTM), int(self.FTA))

    @staticmethod
    def cal_pct(made: int, attempted: int) -> float:
        if attempted != 0:
            return round(made / attempted, 2)
        return 0

    @property
    def data(self):
        return self.__dict__


