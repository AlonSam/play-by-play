class FibaDetailsItem(object):
    """
    class for game data from Segev Sports

    :param dict item: dict with game data
    """

    def __init__(self, item):
        if 'clock' in item:
            item = self.fix_details(item)
        for k, v in item.items():
            setattr(self, k, v)

    def fix_details(self, item):
        game_details = dict()
        home = item['tm']['1']
        away = item['tm']['2']
        game_details['home_team'] = home['name']
        game_details['away_team'] = away['name']
        game_details['home_score'] = home['score']
        game_details['away_score'] = away['score']
        game_details['home_code'] = home['code']
        game_details['away_code'] = away['code']
        game_details['date'] = item['game_date']
        game_details['comp_code'] = item['comp_code']
        game_details['competition'] = item['comp']
        game_details['game_time'] = item['game_time']
        game_details['venue'] = item['venue']
        if 'coachDetails' in home:
            game_details['home_coach'] = home['coachDetails']['firstName'] + " " + home['coachDetails'][
                'familyName']
        if 'coachDetails' in away:
            game_details['away_coach'] = away['coachDetails']['firstName'] + " " + away['coachDetails'][
                'familyName']
        if 'officials_referee1' in item['officials']:
            game_details['referee1'] = item['officials']['referee1']
        if 'officials_referee2' in item:
            game_details['referee2'] = item['officials']['referee2']
        if 'officials_referee3' in item:
            game_details['referee3'] = item['officials']['referee3']
        if 'attendance' in item:
            game_details['attendance'] = item['attendance']
        return game_details

    @property
    def data(self):
        """
        returns game dict
        """
        return self.__dict__