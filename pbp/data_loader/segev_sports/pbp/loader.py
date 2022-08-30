from time import time

from pymongo import MongoClient

from pbp.data_loader.segev_sports.pbp.web import SegevPbpWebLoader
from pbp.resources.pbp.segev_pbp_item import SegevPbpItem


class SegevPbpLoader(object):
    """
    Loads segev_sports pbp data for game
    :param str game_id: segev_sports Game ID
    :param AbsDataLoader source: Where the data should be loaded from - db or web
    """
    client = MongoClient('localhost', 27017)
    db = client.PBP
    data_provider = 'segev_sports'
    resouce = 'pbp'
    parent_object = 'Game'

    def __init__(self, game_id):
        start_time = time()
        self.game_id = game_id
        self.source_data = self._load_data()
        self._make_pbp_items()
        elapsed_time = time() - start_time
        print(f'Elapsed time to load Pbp Events: {elapsed_time}')

    def _load_data(self):
        loader = SegevPbpWebLoader()
        return loader.load_data(self.game_id)

    def _make_pbp_items(self):
        self.items = [SegevPbpItem(**item) for item in self.source_data]
        self.items.sort(key=lambda x: x.event_id)

    @property
    def data(self):
        return [item.dict(by_alias=True) for item in self.items]

