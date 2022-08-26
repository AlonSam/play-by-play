import json
import os
from pathlib import Path

from file_loader import ACBFileLoader
from pbp.resources.boxscore.acb_boxscore_item import ACBBoxScoreItem
from web_loader import ACBWebLoader


class ACBBoxScoreLoader(ACBFileLoader, ACBWebLoader):
    """
    Loads ACB Spanish League boxscore data for game
    :param str game_id: ACB Spanish League Game ID
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
        Loads boxscore data from local file system
        """
        if not self.file_directory:
            raise ValueError('file_directory cannot be None when data source if file')
        self.file_path = f'{self.file_directory}/boxscore.json'
        self._load_data_from_file()
        self._make_boxscore_items()

    def _from_web(self):
        """
        Loads boxscore data from web
        """
        games_file = open("acb auth.txt", encoding='utf-8', mode='r')
        auth = games_file.read()
        games_file.close()
        self.headers = {
            'authorization': auth
        }
        self.base_url = f'https://api2.acb.com/api/v1/openapilive/Boxscore/playermatchstatistics?idCompetition=1&idEdition=85&idMatch={self.game_id}'
        self._load_request_data()

    def _save_data_to_file(self):
        self._make_boxscore_items()
        if self.file_directory:
            if not os.path.isdir(self.file_directory):
                os.makedirs(self.file_directory)
            file_path = f'{self.file_directory}/boxscore.json'
            with open(file_path, 'w') as outfile:
                json.dump(self.data, outfile, indent=4)

    def _make_boxscore_items(self):
        self.items = [ACBBoxScoreItem(item) for item in self.source_data]

    def update_names(self):
        names_path = 'names.json'
        data_file = Path(names_path)
        if not data_file.is_file():
            raise Exception(f'{names_path} does not exist')
        with open(names_path) as json_data:
            names_data = json.load(json_data)
        for item in self.items:
            if item.player_id != item.team_id and item.player_id not in names_data:
                names_data[item.player_id] = item.player
        with open(names_path, 'w') as outfile:
            json.dump(names_data, outfile, indent=4)

    @property
    def data(self):
        return [item.data for item in self.items]

game_id = '101322'
competition = ['ACB', '2020', 'Regular Season']
pbp_loader = ACBBoxScoreLoader(game_id, 'web', competition)
print(pbp_loader.data)