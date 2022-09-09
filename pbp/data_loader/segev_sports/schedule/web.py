import re
import time
from typing import List

from bs4 import BeautifulSoup
from selenium import webdriver

from pbp.data_loader.segev_sports.web_loader import SegevWebLoader

phases_dict = {
    'Regular Season': '5',
    'Quarter Finals': '16',
    'Semi Finals': '26',
    'Finals': '17'
}


class SegevScheduleWebLoader(SegevWebLoader):
    """
    Base class for loading segev_sports schedule saved on database.
    This class should not be instantiated directly.
    """

    def load_data(self, season: str, phase: str) -> List[str]:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        browser = webdriver.Chrome(options=options)
        browser.get(f'https://basket.co.il/results.asp?Board={phases_dict[phase]}&TeamId=0&cYear={season}')
        time.sleep(3)
        page_source = browser.page_source
        browser.quit()
        soup = BeautifulSoup(page_source, 'lxml')
        objects = soup.find_all(href=re.compile('GameId=\d{5}$'))
        game_ids = []
        for object in objects:
            if 'tabindex' in object.attrs.keys():
                game_ids.append(object.attrs['href'][-5:])
        return game_ids

    @property
    def data(self):
        return self.source_data
