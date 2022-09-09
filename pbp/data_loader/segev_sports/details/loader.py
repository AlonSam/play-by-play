from typing import Dict

from pbp.data_loader.segev_sports.details.web import SegevDetailsWebLoader
from pbp.resources.details.segev_details_item import SegevDetailsItem


class SegevDetailsLoader(object):
    """
        Loads segev_sports pbp data for game
        :param str game_id: segev_sports Game ID
        :param str source: Where the data should be loaded from - db or web
        """

    def __init__(self, basket_id: str):
        self.basket_id = basket_id
        self._load_data()

    def _load_data(self):
        source = SegevDetailsWebLoader()
        self.source_data, self.players = source.load_data(self.basket_id)
        self.game_id = str(self.source_data['game_id'])
        self._make_game_item()

    def _make_game_item(self):
        self.item = SegevDetailsItem(**self.source_data)

    @property
    def data(self) -> Dict:
        return self.item.dict(by_alias=True)
