from typing import List

from models.db.stats_model import StatsModel


class EndOfPeriod(object):
    """
    Class for End Of Period events
    """
    event_type = 'endofquarter'

    @property
    def event_stats(self) -> List[StatsModel]:
        """
        returns list of StatsModel object with all stats for event
        """
        return self.base_stats