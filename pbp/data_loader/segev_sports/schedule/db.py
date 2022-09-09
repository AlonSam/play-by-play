from typing import List

from pymongo import MongoClient


class SegevScheduleDBLoader(object):
    """
    Base class for loading segev_sports boxscores saved on database.
    This class should not be instantiated directly.
    """
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        db = self.client.PBP
        self.col = db.games

    def load_data(self, season: str, phase: str) -> List[str]:
        query = {'details.season': season, 'details.phase': phase}
        cursor = self.col.find(query, {'_id': 1})
        self.source_data = []
        for c in cursor:
            self.source_data.append(c['_id'])
        self.client.close()
        return self.source_data

    @property
    def data(self):
        return self.source_data