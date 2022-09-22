from typing import List

import pbp
from models.db.stats_model import StatsModel


class Deflection(object):
    """
    Class for deflection events
    """
    event_type = 'deflection'

    @property
    def event_stats(self) -> List[StatsModel]:
        """
        returns list of StatsModel object with all stats for event
        """
        stats_models = []
        stat_keys = []
        stat_key = pbp.DEFLECTION_STRING
        stat_keys.append(stat_key)
        stat_keys += self._add_misc_stats(stat_key)
        for stat_key in stat_keys:
            stats_models.append(
                StatsModel(
                    player_id=self.player_id,
                    team_id=self.team_id,
                    stat_key=stat_key,
                    stat_value=1
                )
            )
        stats_models = self._add_lineup_data(stats_models)
        return self.base_stats + stats_models