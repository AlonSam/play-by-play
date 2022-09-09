rename_dict = {
    'Stadium': 'venue',
    'Capacity': 'attendance',
    'TeamA': 'home_team',
    'TeamB': 'away_team',
    "CodeTeamA": 'home_code',
    'CodeTeamB': 'away_code',
    'Hour': 'game_time',
    'ScoreA': 'home_score',
    'ScoreB': 'away_score',
    'CoachA': 'home_coach',
    'CoachB': 'away_coach',
}


class ELDetailsItem(object):
    """
    class for game data from Euroleague

    :param dict item: dict with game data
    """

    def __init__(self, item):
        if 'Live' in item:
            item = self.fix_details(item)
        for k, v in item.items():
            setattr(self, k, v)

    def fix_details(self, item):
        item = {rename_dict[k] if k in rename_dict else k.lower(): v for k, v in item.items()}
        item['final'] = not(item['live'])
        item = {k: v for k, v in item.items() if not self.del_keys(k)}
        return item

    @staticmethod
    def del_keys(k):
        unnec_keys = ['ima', 'imb', 'wid', 'gametime', 'live', 'quarter', 'pcom']
        return k in unnec_keys or 'score' in k or 'tv' in k or 'timeout' in k or 'reduce' in k or 'foul' in k

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