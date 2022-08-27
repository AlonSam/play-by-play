from pymongo import MongoClient

from pbp.data_loader.segev_sports.db_loader import SegevDBLoader


class SegevDetailsDBLoader(SegevDBLoader):
    """
    Base class for loading segev_sports boxscores saved on database.
    This class should not be instantiated directly.
    """
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        db = self.client.PBP
        self.col = db.games

    def load_data(self, game_id):
        query = dict(_id=game_id)
        self.source_data = dict(self.col.find_one(query, {'_id': 0, 'details': 1}))
        self.source_data = self.source_data['details']
        self.client.close()
        return self.source_data

    @property
    def data(self):
        return self.source_data
