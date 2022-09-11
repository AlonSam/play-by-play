from datetime import datetime

BASKET_ATTR_MAPPER = {
    'id': 'basket_id',
    'ExternalID': 'game_id',
    'game_year': 'season',
    'game_type': 'phase',
    'GN': 'round',
    'score_team1': 'home_score',
    'score_team2': 'away_score',
    'total_viewers': 'attendance',
    'ref_eng': 'referees',
    'observer_eng': 'observer'
}

TEAM_NAME_MAPPER = {
    'H. BANK YAHAV JERUSALEM': 'Hapoel Jerusalem',
    'NESS ZIONA': 'Ironi Ness Ziona',
    'HAP. UNET-CREDIT HOLON': 'Hapoel Holon',
    'RISHON LEZION': 'Maccabi Rishon Lezion',
    'BEER SHEVA': 'Hapoel Beer Sheva',
    'GILBOA/GALIL': 'Hapoel Gilboa Galil',
    'בני הרצליה': 'Bnei Herzeliya',
    'גלבוע/גליל': 'Hapoel Gilboa Galil',
    "הפ' בי קיור חיפה": 'Hapoel Haifa',
    "הפועל בנק יהב י-ם": "Hapoel Jerusalem",
    "יוסי אברהמי אילת": "Hapoel Eilat",
    'אלטשולר שחם ב"ש': "Hapoel Beer Sheva",
    "מכבי ראשון לציון": "Maccabi Rishon Lezion",
    "מכבי חיפה": "Maccabi Haifa"
}

PHASES_MAPPER = {
    '5': 'Regular Season',
    '16': 'Quarter Finals',
    '26': 'Semi Finals',
    '17': 'Finals'
}


class SegevDetailsItem:
    """
    class for game data from Segev Sports
    :param dict basket_data: dict with game details from basket.co.il
    :param dict segev_data: dict with game details from stats.segevsports
    """
    def __init__(self, basket_data: dict, segev_data: dict):
        self._set_basket_attr(basket_data)
        self._set_segev_attr(segev_data)

    def _set_basket_attr(self, data):
        for key, value in BASKET_ATTR_MAPPER.items():
            if data.get(key) is not None:
                if key == 'ref_eng':
                    setattr(self, value, [ref.strip() for ref in data.get(key).split(',')])
                elif key == 'game_type':
                    setattr(self, value, PHASES_MAPPER[str(data.get(key))])
                else:
                    setattr(self, value, data.get(key))

    def _set_segev_attr(self, data):
        self.final = self.is_finished(data)
        self.time = datetime.strptime(data['time'], '%Y-%m-%dT%H:%M:%S')
        self.home_team = self.fix_name(data['homeTeam']['name'])
        self.away_team = self.fix_name(data['awayTeam']['name'])
        self.home_id = self.fix_name(data['homeTeam']['id'])
        self.away_id = self.fix_name(data['awayTeam']['id'])
        self.competition = data['competition']['name']

    @staticmethod
    def is_finished(data):
        return data['gameFinished'] or data['currentQuarter'] == 4 and data['currentQuarterTime']['m'] == 0 \
               and data['currentQuarterTime']['s'] == 0

    @staticmethod
    def fix_name(tm):
        if tm in TEAM_NAME_MAPPER.keys():
            return TEAM_NAME_MAPPER[tm]
        else:
            names = tm.split(' ')
            team = ''
            for name in names:
                team += name.capitalize() + ' '
            return team.strip()

    @property
    def data(self):
        return self.__dict__

