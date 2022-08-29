from pymongo import MongoClient

from pbp.data_loader.segev_sports.pbp.db import SegevPbpDBLoader
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

    def __init__(self, game_id, source):
        self.game_id = game_id
        self.source = source
        self.source_data = self.source.load_data(self.game_id)
        self._make_pbp_items()

    @classmethod
    def from_web(cls, game_id):
        return cls(game_id, SegevPbpWebLoader())

    @classmethod
    def from_db(cls, game_id):
        return cls(game_id, SegevPbpDBLoader())

    def _make_pbp_items(self):
        self.items = [SegevPbpItem(**item) for item in self.source_data]
        self.items.sort(key=lambda x: x.event_id)

    @property
    def data(self):
        return [item.dict() for item in self.items]

pbp_loader = SegevPbpLoader.from_web('51959')

