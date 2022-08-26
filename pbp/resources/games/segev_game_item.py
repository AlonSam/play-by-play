from datetime import datetime

switch = {
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


class SegevGameItem(object):
    """
    class for game data from Segev Sports

    :param dict item: dict with game data
    """

    def __init__(self, item, basket_data=None):
        if basket_data:
            item = self.fix_details(item, basket_data)
        for k, v in item.items():
            setattr(self, k, v)

    def fix_details(self, item, basket_data):
        new_item = basket_data
        new_item.update({
            'final': self.is_finished(item),
            'time': datetime.strptime(item['time'], '%Y-%m-%dT%H:%M:%S'),
            'home_team': self.fix_name(item['homeTeam']['name']),
            'home_id': int(item['homeTeam']['id']),
            'away_team': self.fix_name(item['awayTeam']['name']),
            'away_id': int(item['awayTeam']['id']),
            'competition': item['competition']['name']
        })
        return new_item

    @staticmethod
    def is_finished(item):
        return item['gameFinished'] or item['currentQuarter'] == 4 and item['currentQuarterTime']['m'] == 0\
        and item['currentQuarterTime']['s'] == 0

    @staticmethod
    def fix_name(tm):
        if tm in switch.keys():
            return switch[tm]
        else:
            names = tm.split(' ')
            team = ''
            for name in names:
                team += name.capitalize() + ' '
            return team.strip()

    @property
    def data(self):
        """
        returns game dict
        """
        return self.__dict__

    @property
    def is_final(self):
        """
        returns True if game is final, false otherwise
        """
        return self.final