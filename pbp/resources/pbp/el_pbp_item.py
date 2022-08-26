rename_dict = {
    'NUMBEROFPLAY': 'event_id',
    'PLAYINFO': 'action_type',
    'PLAYTYPE': 'sub_type',
    'MARKERTIME': 'time',
    'POINTS_A': 'home_score',
    'POINTS_B': 'away_score',
    'MINUTE': 'min',
    'lead': 'margin',
    'DORSAL': 'num',
    'CODETEAM': 'team_code'
}
actions_dict = {
    'BP': ('start', 'period'),
    'TPOFF': 'jumpball',
    'JB': ('jumpball', 'won'),
    '2FGM': '2pt',
    '2FGA': '2pt',
    '3FGM': '3pt',
    '3FGM': '3pt',
    '3FGA': '3pt',
    'AS': 'assist',
    'D': ('rebound', 'defensive'),
    'RV': 'foulon',
    'CM': ('foul', 'personal'),
    'FTM': 'freethrow',
    'FTA': 'freethrow',
    'AG': 'blocked',
    'FV': 'block',
    'O': ('rebound', 'offensive'),
    'TO': 'turnover',
    'ST': 'steal',
    'OUT': ('substitution', 'out'),
    'IN': ('substitution', 'in'),
    'TOUT_TV': ('timeout', 'tv'),
    'EP': ('end', 'period'),
    'TOUT': 'timeout',
    'OF': ('foul', 'offensive'),
    'B': ('foul', 'bench_technical'),
    'EG': ('end', 'game'),
    'BG': ('begin', 'game'),
    'CMU': ('foul', 'unsportsmanlike'),
    'C': ('foul', 'coach_technical'),
    'CMT': ('foul', 'technical')
}


class ELPbpItem(object):
    """
    class for PBP events from Euroleague
    """

    def __init__(self, item, home_team):
        self.home_team = home_team
        if 'NUMBEROFPLAY' in item:
            item = self.fix_event(item)
        delattr(self, 'home_team')
        for k, v in item.items():
            setattr(self, k, v)

    def fix_event(self, event):
        item = {rename_dict[k] if k in rename_dict else k.lower(): v for k, v in event.items()}
        item['player_id'] = item['player_id'].strip()
        item['team_code'] = item['team_code'].strip()
        item['player'] = self.fix_player_name(item['player'])
        item['period'] = self.get_period(item['min'])
        if len(item['time']) > 0:
            item['seconds_remaining'] = self.cal_sec_remaining(item['time'])
        elif 'begin' in item['action_type'].lower():
            item['seconds_remaining'] = 600
        else:
            item['seconds_remaining'] = 0
        if 'x' in item or 'FT' in item['sub_type']:
            if 'x' in item:
                item['shot_value'] = int(item['sub_type'][0])
                self.fix_coords(item)
            if 'M' in item['sub_type']:
                item['made'] = True
            else:
                item['made'] = False
        del item['comment']
        sub = item['sub_type'].strip()
        if isinstance(actions_dict[sub], tuple):
            item['action_type'], item['sub_type'] = actions_dict[sub]
        else:
            item['action_type'] = actions_dict[sub]
            item['sub_type'] = ''
        return item

    @staticmethod
    def cal_sec_remaining(clock):
        min, sec = clock.split(':')
        return int(min) * 60 + int(sec)

    @staticmethod
    def fix_player_name(pl):
        if pl:
            last, first = pl.split(',')
            if len(last.split(' ')) > 1:
                last_names = last.split(' ')
                last = ''
                for nm in last_names:
                    last += nm.capitalize()
                name = f'{first.strip().capitalize()} {last}'
            else:
                name = f'{first.strip().capitalize()} {last.capitalize()}'
            return name

    def fix_coords(self, item):
        if item['team'] == self.home_team:
            x = round(((item['y'] * 776 / 2800) + 56) / 8, 2) - 3
            y = round(((item['x'] * 416 / 1500) + 218) / 4, 2) - 4

        else:
            x = round((800 - (item['y'] * 776 / 2800 + 56)) / 8, 1) + 3
            y = round(((item['x'] * (-416) / 1500) + 218) / 4, 1) - 4
        if x > 50:
            x = 100 - x
        else:
            y = 100 - y
        if x <= 20:
            if y >= 89:
                y -= 3
            elif y <= 11:
                y += 3
            if item['shot_value'] == 3:
                if x >= 12:
                    x += 4
        elif item['shot_value'] == 3:
            x += 2
        else:
            x += 1
        item['x'] = x
        item['y'] = y

    @staticmethod
    def get_period(min):
        if min < 11:
            return 1
        elif min < 21:
            return 2
        elif min < 31:
            return 3
        elif min < 41:
            return 4
        else:
            return 5

    @property
    def data(self):
        return self.__dict__