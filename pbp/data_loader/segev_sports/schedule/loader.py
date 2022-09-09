from pbp.data_loader.abs_data_loader import AbsDataLoader
from pbp.data_loader.segev_sports.schedule.db import SegevScheduleDBLoader
from pbp.data_loader.segev_sports.schedule.web import SegevScheduleWebLoader


class SegevScheduleLoader(object):
    """
        Loads segev_sports list of details for given season and phase
        :param str season: season
        :param str phase: phase of season
        :param str source: Where the data should be loaded from - db or web
        """
    data_provider = 'segev_sports'
    resource = 'schedule'
    parent_object = 'Season'

    def __init__(self, season: str, phase: str, source: AbsDataLoader):
        self.season = season
        self.phase = phase
        self.source = source
        self.items = self.source.load_data()

    @classmethod
    def from_web(cls, season: str, phase: str):
        return cls(season, phase, SegevScheduleWebLoader())

    @classmethod
    def from_db(cls, season: str, phase: str):
        return cls(season, phase, SegevScheduleDBLoader())

    @property
    def data(self):
        return self.items
