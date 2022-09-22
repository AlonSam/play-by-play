from abc import abstractmethod
from typing import List

import pbp
from models.db.stats_model import StatsModel
from pbp.exceptions import MissedShotNotFound
from pbp.resources.events.field_goal import FieldGoal
from pbp.resources.events.free_throw import FreeThrow


class Rebound(object):
    """
    class for Rebound events
    """
    event_type = 'rebound'

    @property
    @abstractmethod
    def is_offensive(self):
        pass

    @property
    @abstractmethod
    def is_defensive(self):
        pass

    @property
    def missed_shot(self):
        """
        returns FieldGoal or FreeThrow object for shot that was missed
        """
        if isinstance(self.previous_event, (FieldGoal, FreeThrow)):
            if not self.previous_event.is_made:
                return self.previous_event
            else:
                raise (f'Rebound after made shot: {self.game_id}-Q{self.period}-{self.time}')
        else:
            previous_event = self.previous_event
            while previous_event and not isinstance(previous_event, (FieldGoal, FreeThrow)):
                previous_event = previous_event.previous_event
            if not previous_event.is_made:
                return previous_event
            raise MissedShotNotFound(f'{self.game_id}-Q{self.period}-{self.time}')

    @property
    def self_reb(self):
        """
        returns True if rebound was grabbed by the same player who missed the shot, False otherwise
        """
        return self.player_id == self.missed_shot.player_id

    @property
    def is_team_rebound(self):
        return self.team_id == '0'

    @property
    def missed_shot_event_id(self):
        return self.missed_shot.event_id

    @property
    def missed_shot_zone(self):
        if isinstance(self.missed_shot, FieldGoal):
            return self.missed_shot.shot_zone
        return 'FreeThrow'

    @property
    def event_stats(self) -> List[StatsModel]:
        """
        returns list of StatsModel object with all stats for event
        """
        stats_models = []
        basic_shot_zone = self.missed_shot.basic_shot_zone
        if isinstance(self.missed_shot, FieldGoal) and self.missed_shot.is_blocked:
            if not self.is_offensive:
                blocked_recovered_key = pbp.BLOCKED_STRING + basic_shot_zone + "Recovered"
                stats_models.append(
                    StatsModel(
                        player_id=self.missed_shot.block_player_id,
                        team_id=self.team_id,
                        stat_key=blocked_recovered_key,
                        stat_value=1
                    )
                )
            basic_shot_zone += pbp.BLOCKED_STRING
        if self.is_offensive:
            team_abbreviation = pbp.OFFENSIVE_ABBREVIATION_PREFIX
            opponent_abbreviation = pbp.DEFENSIVE_ABBREVIATION_PREFIX
        else:
            team_abbreviation = pbp.DEFENSIVE_ABBREVIATION_PREFIX
            opponent_abbreviation = pbp.OFFENSIVE_ABBREVIATION_PREFIX
        rebound_key = team_abbreviation + basic_shot_zone + pbp.REBOUNDS_STRING
        opportunity_key = team_abbreviation + basic_shot_zone + pbp.REBOUND_OPPORTUNITIES_STRING
        opponent_opportunity_key = opponent_abbreviation + basic_shot_zone + pbp.REBOUND_OPPORTUNITIES_STRING
        stats_models.append(
            StatsModel(
                player_id=self.player_id,
                team_id=self.team_id,
                stat_key=rebound_key,
                stat_value=1
            )
        )
        for team_id, player_ids in self.players_on_court.items():
            stat_key = opportunity_key if team_id == self.team_id else opponent_opportunity_key
            for player_id in player_ids:
                stats_models.append(
                    StatsModel(
                        player_id=player_id,
                        team_id=team_id,
                        stat_key=stat_key,
                        stat_value=1
                    )
                )
        self_off_rebound_opportunity_key = pbp.SELF_STRING + pbp.OFFENSIVE_ABBREVIATION_PREFIX + pbp.REBOUND_OPPORTUNITIES_STRING
        self_off_rebound_stat_keys = [self_off_rebound_opportunity_key]
        if self.self_reb:
            self_rebounded_key = pbp.SELF + pbp.OFFENSIVE_ABBREVIATION_PREFIX + pbp.REBOUNDS_STRING
            self_off_rebound_stat_keys.append(self_rebounded_key)
        for self_off_rebound_stat_key in self_off_rebound_stat_keys:
            stats_models.append(
                StatsModel(
                    player_id=self.missed_shot.player_id,
                    team_id=self.missed_shot.team_id,
                    stat_key=self_off_rebound_stat_key,
                    stat_value=1
                )
            )
        stats_models = self._add_lineup_data(stats_models)
        return self.base_stats + stats_models


