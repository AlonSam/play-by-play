import json
import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from pbp.data_loader.fiba.file_loader import FibaFileLoader
from pbp.data_loader.fiba.web_loader import FibaWebLoader
from pbp.resources.games.fiba_game_item import FibaGameItem

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)


class FibaDetailLoader(FibaFileLoader, FibaWebLoader):
    """
        Loads FIBA Live Stats data for game
        :param str game_id: FIBA Live Stats Game ID
        :param str source: Where the data should be loaded from - file or web
        :param lst competition: List that contains the name of competition, season, phase and FIBA Code.
        :param bool intl: True if International strings are needed, False otherwise
        """
    base_directory = 'C:/Users/alons/PBP Database/'

    def __init__(self, game_id, source, competition, intl):
        self.game_id = game_id
        self.source = source
        self.competition = competition
        self.intl = intl
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
        self.base_url = f'http://www.fibalivestats.com/data/{self.game_id}/data.json'
        self._load_request_data()

    def get_basic_details(self):
        """
        extract date, venue and competition from game's page
        """
        if len(self.competition) < 4:
            raise Exception('No Code included')
        else:
            code = self.competition[3]
            basic_url = f'https://www.fibalivestats.com/u/{code}/{self.game_id}/'
            if self.intl:
                suffix = 'pbp_en_AU.html'
            else:
                suffix = 'pbp.html'
            response = requests.get(basic_url + suffix)
            if response.status_code == 200:
                page_source = response.content
                soup = BeautifulSoup(page_source, 'lxml')
                comp = soup.find('div', attrs={'class': 'matchDetail'})
                basic_detail = {}
                basic_detail['comp'] = comp.contents[3].text
                basic_detail['comp_code'] = code
                venue = comp.find_next("div")
                if "Venue" in venue.text:
                    basic_detail['venue'] = venue.contents[3].text
                    game_date = venue.find_next("div")
                    game_time = game_date.contents[3].text.split('\n')[0]
                    game_time = game_time.split(': ')[1].strip()
                    basic_detail['game_time'] = game_time
                    date = game_date.contents[3].text.split('\n')[1].strip()
                else:
                    game_time = venue.contents[3].text.split('\n')[0]
                    game_time = game_time.split(': ')[1].strip()
                    basic_detail['game_time'] = game_time
                    date = venue.contents[3].text.split('\n')[1].strip()
                basic_detail['game_date'] = date
                return basic_detail
            else:
                response.raise_for_status()

    def _save_data_to_file(self):
        self.source_data.update(self.get_basic_details())
        self._make_game_item()
        if self.file_directory and os.path.isdir(self.file_directory):
            file_path = f'{self.file_directory}/details.json'
            with open(file_path, 'w') as outfile:
                json.dump(self.data, outfile, indent=4)

    def _make_game_item(self):
        self.item = FibaGameItem(self.source_data)

    @property
    def data(self):
        return self.item.data


game_id = '1758418'
competition = ['Champions League', '2020', 'Qualifiers', 'FEUR']
pbp_loader = FibaDetailLoader(game_id, 'web', competition, False)
print(pbp_loader.data)