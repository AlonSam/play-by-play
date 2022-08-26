from pymongo import MongoClient

from pbp.data_loader.segev_sports.pbp.db import SegevPbpDBLoader
from pbp.data_loader.segev_sports.pbp.web import SegevPbpWebLoader
from pbp.resources.pbp.segev_pbp_item import SegevPbpItem


class SegevPbpLoader(object):
    """
    Loads segev_sports pbp data for game
    :param str game_id: segev_sports Game ID
    :param str source: Where the data should be loaded from - db or web
    :param lst competition: List that contains the name of competition, season and phase in season.
    """
    client = MongoClient('localhost', 27017)
    db = client.PBP
    data_provider = 'segev_sports'
    resouce = 'pbp'
    parent_object = 'Game'

    def __init__(self, game_id, source='web'):
        self.game_id = game_id
        self.source = source
        self.source_data = self._load_data()
        self._make_pbp_items()

    def _load_data(self):
        if self.source == 'web':
            source_loader = SegevPbpWebLoader()
        else:
            source_loader = SegevPbpDBLoader()
        return source_loader.load_data(self.game_id)

    def _make_pbp_items(self):
        if 'result' in self.source_data.keys():
            self.source_data = self.source_data['result']['actions']
            not_imp = ['clock', 'game']
            self.items = [SegevPbpItem(item) for item in self.source_data if item['type'] not in not_imp]
            self.items.sort(key=lambda x: x.event_id)
        else:
            self.items = [SegevPbpItem(item) for item in self.source_data]

    @property
    def data(self):
        return [item.data for item in self.items]