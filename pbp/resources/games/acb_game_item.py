from datetime import datetime

rename_dict = {
    'id': 'game_id',
    'local_points': 'home_score',
    'visitor_points': 'away_score',
    'matchweek_number': 'round',
    'crowd': 'attendance',
    'start_date': 'date',
    'finalized': 'final',
    'time': 'game_time'
}


class ACBGameItem(object):
    """
    class for game data from ACB Spanish League

    :param dict item: dict with game data
    """

    def __init__(self, item):
        if 'edition' in item:
            item = self.fix_details(item)
        for k, v in item.items():
            setattr(self, k, v)

    def fix_details(self, item):
        new_item = {rename_dict[k]: v for k, v in item.items() if k in rename_dict}
        new_item['date'] = datetime.utcfromtimestamp(new_item['date']).strftime('%Y-%m-%d')
        new_item['game_time'] = datetime.utcfromtimestamp(new_item['game_time']).strftime('%H:%M:%S')
        new_item['competition'] = item['competition']['official_name']
        new_item['phase'] = item['phase']['description']
        new_item['season'] = item['edition']['year']
        new_item['venue'] = item['arena']['name']
        new_item['home_team'] = item['team1']['team_actual_name']
        new_item['away_team'] = item['team2']['team_actual_name']
        new_item['home_code'] = item['team1']['team_abbrev_name']
        new_item['away_code'] = item['team2']['team_abbrev_name']
        new_item['home_coach'] = item['team1']['coaches'][-1]['license']['licenseStr15']
        new_item['away_coach'] = item['team2']['coaches'][-1]['license']['licenseStr15']
        for i in range(len(item['referee'])):
            new_item[f'referee{i+1}'] = item['referee'][i]['license']['licenseStr15']
        return new_item

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