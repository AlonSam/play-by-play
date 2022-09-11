KEY_ATTR_MAPPER = {
    "playerId": "player_id",
    "jerseyNumber": "shirt_num",
    "minutes": "min",
    "plusMinus": "plus_minus",
    "fb": "fastbreak_pts",
    "points": "pts",
    "rate": "pir",
    "sc": "second_chance_pts",
    "Points_from_turnovers": "turnover_pts",
    "Points_in_the_paint": "points_in_the_paint",
    "Second_chance_points": "second_chance_pts",
    }

KEYS = ['team_id', 'game_id', 'ast', 'to', 'stl', 'dunk', 'dfl', 'rec', 'vps']


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
        data['treb'] = data['reb_o'] + data['reb_d']
        data['threepa'] = data['fg_3m'] + data['fg_3mis']
        data['twopa'] = data['fg_2m'] + data['fg_2mis']
        data['fta'] = data['ft_m'] + data['ft_mis']
        data['fgm'] = data['fg_2m'] + data['fg_3m']
        data['fga'] = data['twopa'] + data['threepa']
        data['twopct'] = self.cal_pct(data['fg_2m'], data['twopa'])
        data['threepct'] = self.cal_pct(data['fg_3m'], data['threepa'])
        data['fgpct'] = self.cal_pct(data['fgm'], data['fga'])
        data['ftpct'] = self.cal_pct(data['ft_m'], data['fta'])
        self.reb = dict(treb=data['treb'], dreb=data['reb_d'], oreb=data['reb_o'])
        self.fg = dict(made=data['fgm'], attempted=data['fga'], pct=data['fgpct'])
        self.two_pt = dict(made=data['fg_2m'], attempted=data['twopa'], pct=data['twopct'])
        self.three_pt = dict(made=data['fg_3m'], attempted=data['threepa'], pct=data['threepct'])
        self.ft = dict(made=data['ft_m'], attempted=data['fta'], pct=data['ftpct'])
        self.fouls = dict(made=data['f'], drawn=data['f_drawn'])
        self.blocks = dict(made=data['blk'], blocked=data['blk_against'])

    @staticmethod
    def cal_pct(made: int, attempted: int) -> float:
        if attempted != 0:
            return round(made / attempted, 2)
        return 0

    @property
    def data(self):
        return self.__dict__


