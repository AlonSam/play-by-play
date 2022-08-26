import json
import os

from file_loader import ACBFileLoader
from pbp.resources.games.acb_game_item import ACBGameItem
from web_loader import ACBWebLoader


class ACBGameLoader(ACBFileLoader, ACBWebLoader):
    """
    Loads ACB Spanish League data for game
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

    def _load_data(self):
        source_method = getattr(self, f'_from_{self.source}')
        source_method()

    def _from_file(self):
        """
        Loads game data from local file system
        """
        if not self.file_directory:
            raise ValueError('file_directory cannot be None when data source if file')
        self.file_path = f'{self.file_directory}/details.json'
        self._load_data_from_file()
        self._make_game_item()

    def _from_web(self):
        """
        Loads game data from web
        """
        games_file = open("acb auth.txt", encoding='utf-8', mode='r')
        auth = games_file.read()
        games_file.close()
        self.headers = {
            'authorization': auth
        }
        self.base_url = f'https://api2.acb.com/api/v1/openapilive/Matches/matchlite?idMatch={self.game_id}'
        self._load_request_data()

    def _save_data_to_file(self):
        self._make_game_item()
        if self.file_directory:
            if not os.path.isdir(self.file_directory):
                os.makedirs(self.file_directory)
            file_path = f'{self.file_directory}/details.json'
            with open(file_path, 'w') as outfile:
                json.dump(self.data, outfile, indent=4)

    def _make_game_item(self):
        self.item = ACBGameItem(self.source_data)

    @property
    def data(self):
        return self.item.data

game_id = '101323'
competition = ['ACB', '2020', 'Regular Season']
pbp_loader = ACBGameLoader(game_id, 'web', competition)
print(pbp_loader.data)