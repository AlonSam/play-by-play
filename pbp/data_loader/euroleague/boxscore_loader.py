import json
import os

import requests
from bs4 import BeautifulSoup

from file_loader import ELFileLoader
from pbp.resources.boxscore.el_boxscore_item import ELBoxScoreItem
from web_loader import ELWebLoader


class ELBoxScoreLoader(ELFileLoader, ELWebLoader):
    """
    Loads Euroleague Box Score data
    :param str game_id: Euroleague Game ID
    :param str source: Where the data should be loaded from - file or web
    :param lst competition: List that contains the name of competition (EL or EC), season and phase in season.
    """
    base_directory = 'C:/Users/alons/PBP Database/'

    def __init__(self, game_id, source, competition):
        self.game_id = game_id
        self.source = source
        self.competition = competition
        self.file_directory = self.base_directory + f'{competition[0]}/{competition[1]}/{game_id}'
        self.source_data = []
        self._load_data()

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
        if self.competition[0] == 'Euroleague':
            season = 'E' + self.competition[1]
            self.base_url = f'https://www.euroleague.net/main/results/showgame?gamecode={self.game_id}&seasoncode={season}'
        else:
            season = 'U' + self.competition[1]
            self.base_url = f'https://www.eurocupbasketball.com/eurocup/games/results/showgame?gamecode={self.game_id}&seasoncode={season}'
        response = requests.get(self.base_url)
        if response.status_code == 200:
            page_source = response.content
            soup = BeautifulSoup(page_source, 'lxml')
            self.make_boxscore_dict(soup)
            self._save_data_to_file()
        else:
            response.raise_for_status()

    def make_boxscore_dict(self, soup):
        teams = soup.find_all('div', attrs={'class': 'eu-team-stats-teamname'})
        teams = [tm.text.strip('\n') for tm in teams]
        tbl = soup.find_all('table', attrs={'id': 'tblPlayerPhaseStatistics'})
        self.extract_data(tbl[0], teams[0])
        self.extract_data(tbl[1], teams[1])

    def extract_data(self, tbl, tm):
        key_list = ['num', 'player', 'min', 'pts', 'twopm', 'twopa', 'threepm', 'threepa', 'ftm', 'fta', 'oreb', 'dreb',
                    'treb', 'ast', 'stl', 'tov', 'blk', 'blkd', 'pf', 'fd', 'pir']
        player_list = tbl.find_all('tr')
        player_list = [pl.text for pl in player_list[2:-1]]
        for pl in player_list:
            data = pl.split('\n')
            bs_dict = {k: 0 for k in key_list}
            j = 0
            if data[3] == 'DNP':
                continue
            for i in range(1, len(data) - 1):
                if len(data[i]) > 0 and data[i] != '\xa0':
                    if '/' in data[i]:
                        made, attempted = data[i].split('/')
                        bs_dict[key_list[j]] = int(made)
                        bs_dict[key_list[j + 1]] = int(attempted)
                    elif data[i].isnumeric():
                        bs_dict[key_list[j]] = int(data[i])
                    else:
                        bs_dict[key_list[j]] = data[i]
                if 8 > i > 4:
                    j += 2
                else:
                    j += 1
            bs_dict['team'] = tm
            self.source_data.append(bs_dict)

    def _save_data_to_file(self):
        self._make_boxscore_items()
        if self.file_directory:
            if not os.path.isdir(self.file_directory):
                os.makedirs(self.file_directory)
            file_path = f'{self.file_directory}/boxscore.json'
            with open(file_path, 'w') as outfile:
                json.dump(self.data, outfile, indent=4)

    def _make_boxscore_items(self):
        self.items = [ELBoxScoreItem(item) for item in self.source_data]


    @property
    def data(self):
        return [item.data for item in self.items]

game_id = '211'
competition = ['Euroleague', '2020', 'Regular Season']
pbp_loader = ELBoxScoreLoader(game_id, 'web', competition)
print(pbp_loader.data)