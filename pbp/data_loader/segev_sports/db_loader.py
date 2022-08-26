from pymongo import MongoClient

from pbp.data_loader.abs_data_loader import AbsDataLoader


class SegevDBLoader(AbsDataLoader):
    """
    Base class for loading segev_sports files saved on database.
    This class should not be instantiated directly.
    """

    def _load_data_from_db(self, col_name, query):
        client = MongoClient('localhost', 27017)
        db = client.PBP
        col = db[col_name]
        self.source_data = dict(col.find_one(query))
        client.close()

    @property
    def data(self):
        return self.source_data