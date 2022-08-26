import json
import os
from pathlib import Path

from file_loader import FibaFileLoader
from pbp.resources.boxscore.fiba_boxscore_item import FibaBoxScoreItem
from web_loader import FibaWebLoader


class FibaBoxScoreLoader(FibaFileLoader, FibaWebLoader):
    """
    Loads FIBA Live Stats box score data for game
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
        self.update_names()

    def _load_data(self):
        source_method = getattr(self, f'_from_{self.source}')
        source_method()

    def _from_file(self):
        """
        Loads pbp data from local file system
        """
        if not self.file_directory:
            raise ValueError('file_directory cannot be None when data source if file')
        self.file_path = f'{self.file_directory}/boxscore.json'
        self._load_data_from_file()
        self._make_boxscore_items()

    def _from_web(self):
        """
        Loads pbp data from web
        """
        self.base_url = f'http://www.fibalivestats.com/data/{self.game_id}/data.json'
        self._load_request_data()

    def extract_boxscore(self):
        self.source_data = self.source_data['tm']

    def _save_data_to_file(self):
        self.extract_boxscore()
        self._make_boxscore_items()
        if self.file_directory:
            if not os.path.isdir(self.file_directory):
                os.makedirs(self.file_directory)
            file_path = f'{self.file_directory}/boxscore.json'
            with open(file_path, 'w') as outfile:
                json.dump(self.data, outfile, indent=4)

    def _make_boxscore_items(self):
        if '1' in self.source_data:
            home_players = self.source_data['1']['pl']
            home_name = self.source_data['1']['name']
            away_players = self.source_data['2']['pl']
            away_name = self.source_data['2']['name']
            home_team = {k[4:]: v for k, v in self.source_data['1'].items() if 'tot_' in k and 'eff' not in k}
            away_team = {k[4:]: v for k, v in self.source_data['2'].items() if 'tot_' in k and 'eff' not in k}
            self.items = [FibaBoxScoreItem(home_players[item], home_name) for item in home_players]
            self.items += [FibaBoxScoreItem(away_players[item], away_name) for item in away_players]
            self.items.append(FibaBoxScoreItem(home_team, home_name))
            self.items.append(FibaBoxScoreItem(away_team, away_name))
        else:
            self.items = [FibaBoxScoreItem(item) for item in self.source_data]

    def update_names(self):
        names_path = 'names.json'
        data_file = Path(names_path)
        if not data_file.is_file():
            raise Exception(f'{names_path} does not exist')
        with open(names_path) as json_data:
            names_data = json.load(json_data)
        for item in self.items:
            d = item.data
            if 'num' in d:
                key = d['team_name'] + d['num']
                if key not in names_data:
                    names_data[key] = d['player']
        with open(names_path, 'w') as outfile:
            json.dump(names_data, outfile, indent=4)

    @property
    def data(self):
        return [item.data for item in self.items]

game_id = '1758418'
competition = ['Champions League', '2020', 'Qualifiers']
pbp_loader = FibaBoxScoreLoader(game_id, 'file', competition)
print(pbp_loader.data)
