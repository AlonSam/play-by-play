from pbp.data_loader.segev_sports.schedule.db import SegevScheduleDBLoader
from pbp.data_loader.segev_sports.schedule.web import SegevScheduleWebLoader


class SegevScheduleLoader(object):
    """
        Loads segev_sports list of games for given season and phase
        :param str season: season
        :param str phase: phase of season
        :param str source: Where the data should be loaded from - db or web
        """
    data_provider = 'segev_sports'
    resource = 'schedule'
    parent_object = 'Season'

    def __init__(self, season, phase, source='web'):
        self.season = season
        self.phase = phase
        self.source = source
        self.items = self.load_data()

    def load_data(self):
        if self.source == 'web':
            source_loader = SegevScheduleWebLoader()
        else:
            source_loader = SegevScheduleDBLoader()
        return source_loader.load_data(self.season, self.phase)

    @property
    def data(self):
        return self.items
