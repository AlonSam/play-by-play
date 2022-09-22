from typing import List

from models.db.stats_model import StatsModel


class Timeout(object):
    """
    Class for Timeout events
    """
    event_type = 'timeout'

    @property
    def event_stats(self) -> List[StatsModel]:
        """
        returns list of StatsModel object with all stats for event
        """
        return self.base_stats