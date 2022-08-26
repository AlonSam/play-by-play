import json
import os

from file_loader import FibaFileLoader
from pbp.resources.pbp.fiba_pbp_item import FibaPbpItem
from web_loader import FibaWebLoader


class FibaPbpLoader(FibaFileLoader, FibaWebLoader):
    """
    Loads FIBA Live Stats pbp data for game
    :param str game_id: FIBA Live Stats Game ID
    :param str source: Where the data should be loaded from - file or web
    :param lst competition: List that contains the name of competition, season and phase in season.
    """
    base_directory = 'C:/Users/alons/PBP Database/'

    def __init__(self, game_id, source, competition):
        self.game_id = game_id
        self.source = source
        self.competition = competition
        self.file_directory = self.base_directory + f'{competition[0]}/{competition[1]}/{game_id}'
        self._load_data()

    def _load_data(self):
        source_method = getattr(self, f'_from_{self.source}')
        source_method()

    def _from_file(self):
        """
        Loads pbp data from local file system
        """
        if not self.file_directory:
            raise ValueError('file_directory cannot be None when data source if file')
        self.file_path = f'{self.file_directory}/playbyplay.json'
        self._load_data_from_file()
        self._make_pbp_items()

    def _from_web(self):
        """
        Loads pbp data from web
        """
        self.base_url = f'http://www.fibalivestats.com/data/{self.game_id}/data.json'
        self._load_request_data()

    def extract_actions(self):
        home_team = self.source_data['tm']['1']['name']
        away_team = self.source_data['tm']['2']['name']
        for item in self.source_data['pbp']:
            if item['tno'] == 1:
                item['team'] = home_team
            elif item['tno'] == 2:
                item['team'] = away_team
        shot_list = [ev for ev in self.source_data['tm']['1']['shot']]
        shot_list += [ev for ev in self.source_data['tm']['2']['shot']]
        self.source_data = self.source_data['pbp']
        self.source_data.reverse()
        for item in self.source_data:
            if 'actionType' in item and 'pt' in item['actionType']:
                p = [ev for ev in shot_list if item['actionNumber'] == ev['actionNumber']]
                ev = p[0]
                item['x'] = round(ev['x'], 2)
                item['y'] = round(ev['y'], 2)

    def _save_data_to_file(self):
        self.extract_actions()
        self._make_pbp_items()
        if self.file_directory:
            if not os.path.isdir(self.file_directory):
                os.makedirs(self.file_directory)
            file_path = f'{self.file_directory}/playbyplay.json'
            with open(file_path, 'w') as outfile:
                json.dump(self.data, outfile, indent=4)

    def _make_pbp_items(self):
        self.items = [FibaPbpItem(item) for item in self.source_data]
        self.items.sort(key=lambda x: x.event_id)

    @property
    def data(self):
        return [item.data for item in self.items]

game_id = '1758418'
competition = ['Champions League', '2020', 'Qualifiers']
pbp_loader = FibaPbpLoader(game_id, 'web', competition)