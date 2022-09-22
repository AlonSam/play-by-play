from typing import List

from models.db.stats_model import StatsModel


class StartOfPeriod(object):
    """
    Class for start of period events
    """
    event_type = 'startofquarter'

    @property
    def event_stats(self) -> List[StatsModel]:
        """
        returns list of StatsModel object with all stats for event
        """
        return self.base_stats