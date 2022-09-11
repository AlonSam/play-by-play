import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver

from pbp.data_loader.segev_sports.loader import SegevLoader

PHASES_MAPPER = {
    'Regular Season': '5',
    'Quarter Finals': '16',
    'Semi Finals': '26',
    'Finals': '17'
}


class SegevScheduleLoader(SegevLoader):
    """
        Loads segev_sports list of details for given season and phase
        :param str season: season
        :param str phase: phase of season
        """

    def __init__(self, season: str, phase: str):
        self.season = season
        self.phase = phase
        self.items = self._load_data()

    def _load_data(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        browser = webdriver.Chrome(options=options)
        browser.get(f'https://basket.co.il/results.asp?Board={PHASES_MAPPER[self.phase]}&TeamId=0&cYear={self.season}')
        time.sleep(3)
        page_source = browser.page_source
        browser.quit()
        soup = BeautifulSoup(page_source, 'lxml')
        finished_games = soup.find_all('table', {'class': 'stats_tbl'})[1]
        games = finished_games.find_all(href=re.compile('GameId=\d{5}$'))
        game_ids = [game.attrs['href'][-5:] for game in games]
        # for game in games:
        #     if 'tabindex' in game.attrs.keys():
        #         game_ids.append(game.attrs['href'][-5:])
        return game_ids

    @property
    def data(self):
        return self.items
