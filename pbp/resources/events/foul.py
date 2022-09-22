from typing import List

import pbp
from models.db.stats_model import StatsModel


class Foul(object):
    """
    class for foul events
    """
    event_type = 'foul'

    @property
    def foul_type_string(self):
        if self.is_personal_foul:
            return pbp.PERSONAL_FOUL_TYPE_STRING
        if self.is_shooting_foul:
            return pbp.SHOOTING_FOUL_TYPE_STRING
        if self.is_offensive_foul:
            return pbp.OFFENSIVE_FOUL_TYPE_STRING
        if self.is_technical:
            return pbp.TECHNICAL_FOUL_TYPE_STRING
        if self.is_unsportsmanlike_foul:
            return pbp.UNSPORTSMANLIKE_FOUL_TYPE_STRING
        if self.is_and_one_foul:
            return pbp.AND_ONE_FOUL_TYPE_STRING

    @property
    def event_stats(self) -> List[StatsModel]:
        """
        returns list of StatsModel object with all stats for event
        """
        stats_models = []
        stat_keys = []
        foul_type = self.foul_type_string
        is_over_the_limit = self.is_over_the_limit_event
        if foul_type is not None:
            stat_keys.append(foul_type)
            fouls_stat_key = pbp.FOULS_STRING
            stat_keys.append(fouls_stat_key)
            if is_over_the_limit:
                stat_keys.append(f'{pbp.OVER_THE_LIMIT_STRING}{foul_type}')
                stat_keys.append(f'{pbp.OVER_THE_LIMIT_STRING}{fouls_stat_key}')
            for stat_key in stat_keys:
                stats_models.append(
                    StatsModel(
                        player_id=self.player_id,
                        team_id=self.team_id,
                        stat_key=stat_key,
                        stat_value=1
                    )
                )
            team_ids = list(self.players_on_court.keys())
            if hasattr(self, 'foul_on_player_id'):
                foul_on_player_id = self.foul_on_player_id
                stat_keys = []
                foul_on_stat_key = foul_type + pbp.DRAWN_TYPE_STRING
                fouls_drawn_stat_key = pbp.FOULS_STRING + pbp.DRAWN_TYPE_STRING
                stat_keys.append(foul_on_stat_key)
                stat_keys.append(fouls_drawn_stat_key)
                opponent_team_id = team_ids[0] if self.team_id == team_ids[1] else team_ids[1]
                if foul_on_player_id in self.players_on_court[self.team_id]:
                    team = self.team_id
                else:
                    team = opponent_team_id
                if is_over_the_limit:
                    stat_keys.append(f'{pbp.OVER_THE_LIMIT_STRING}{foul_on_stat_key}')
                    stat_keys.append(f'{pbp.OVER_THE_LIMIT_STRING}{fouls_drawn_stat_key}')
                for stat_key in stat_keys:
                    stats_models.append(
                        StatsModel(
                            player_id=foul_on_player_id,
                            team_id=team,
                            stat_key=stat_key,
                            stat_value=1
                        )
                    )
            stats_models = self._add_lineup_data(stats_models)
            return self.base_stats + stats_models


