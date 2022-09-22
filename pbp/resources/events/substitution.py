from typing import List

from models.db.stats_model import StatsModel


class Substitution(object):
    """
    class for substitution events
    """

    event_type = 'substitution'

    @property
    def players_on_court(self):
        """
        returns dict with an updated list of player ids of each team
        """
        pass

    @property
    def event_stats(self) -> List[StatsModel]:
        """
        returns list of StatsModel object with all stats for event
        """
        return self.base_stats