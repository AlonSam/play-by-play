import pbp
from pbp.data_loader.segev_sports.web_loader import SegevWebLoader

phases_dict = {
    '5': 'Regular Season',
    '16': 'Quarter Finals',
    '26': 'Semi Finals',
    '17': 'Finals'
}


class SegevDetailsWebLoader(SegevWebLoader):
    """
    Base class for loading segev_sports details saved on database.
    This class should not be instantiated directly.
    """

    def load_data(self, game_id):
        self.base_url = pbp.SEGEV_ACTIONS_BASE_URL + game_id
        self.source_data = self._load_request_data()
        self.source_data = self.source_data['result']['gameInfo']
        return self.source_data

    def load_basket_data(self, basket_id):
        self.base_url = pbp.BASKET_GAME_DATA_BASE_URL + basket_id
        base_data = self._load_request_data()
        base_data = base_data[0]['games'][0]
        self.basket_data = {
            'basket_id': base_data['id'],
            'game_id': int(base_data['ExternalID']),
            'season': str(base_data['game_year']),
            'phase': phases_dict[str(base_data['game_type'])],
            'round': base_data['GN'],
            'home_score': base_data['score_team1'],
            'away_score': base_data['score_team2'],
            'attendance': base_data['total_viewers'],
            'referees': [ref.strip() for ref in base_data['ref_eng'].split(',')],
            'observer': base_data['observer_eng'].strip()
        }
        return self.basket_data



    @property
    def data(self):
        return self.source_data