from abc import ABCMeta, abstractmethod
from typing import List

import pbp
import pbp.resources.events as e
from models.db.stats_model import StatsModel
from pbp.resources.events.field_goal import FieldGoal
from pbp.resources.events.foul import Foul
from pbp.resources.events.free_throw import FreeThrow
from pbp.resources.events.rebound import Rebound


class EventItem(metaclass=ABCMeta):
    """
    An Abstract Class for all enhanced pbp event types
    """

    @property
    @abstractmethod
    def is_possession_ending_event(self):
        """
        returns True if event ends a possession, False otherwise
        """
        pass

    @abstractmethod
    def get_all_related_events(self):
        """
        returns list of all directly related events to current event (FIBA & Segev Sports only)
        """
        pass

    def get_all_events_at_current_time(self) -> list:
        """
        returns list of all events that take place at the same time as the current event
        """
        events = []
        # going backwards
        event = self
        while event and self.seconds_remaining == event.seconds_remaining:
            if event != self:
                events.append(event)
            event = event.previous_event
        # going forwards
        event = self
        while event and self.seconds_remaining == event.seconds_remaining:
            if event != self:
                events.append(event)
            event = event.next_event
        return sorted(events, key=lambda k: k.event_id)

    @property
    def players_on_court(self) -> dict:
        """
        returns dict with list of player ids for each team with players on court for current event
        For all non substitution events on court players are just the same as previous event
        This function gets overwritten in events.substitution.Subsitutiton
        """
        return self.previous_event.players_on_court.copy()

    @property
    def seconds_remaining(self) -> int:
        min, sec = self.time.split(':')
        return int(min) * 60 + int(sec)

    @property
    def seconds_since_previous_event(self) -> int:
        """
        returns the number of seconds that have elapsed since the previous event
        """
        if not self.previous_event:
            return 0
        if self.seconds_remaining == 600:
            return 0
        if self.seconds_remaining == 300 and self.period > 4:
            return 0
        return self.previous_event.seconds_remaining - self.seconds_remaining

    @property
    def is_second_chance_event(self) -> bool:
        """
        return True if the event takes place after an offensive rebound
        on the current possession, False otherwise
        """
        event = self.previous_event
        if isinstance(event, Rebound) and event.sub_type == e.OFFENSIVE_STRING:
            return True
        while event and not event.is_possession_ending_event:
            if isinstance(event, Rebound) and event.sub_type == e.OFFENSIVE_STRING:
                return True
            event = event.previous_event
        return False

    @property
    def is_over_the_limit_event(self) -> bool:
        """
        returns True if the team on defense is over the limit (no fouls to give), False otherwise
        """
        if hasattr(self, 'fouls_to_give'):
            team_ids = list(self.players_on_court.keys())
            offense_team_id = self.offense_team_id
            defense_team_id = (team_ids[0] if offense_team_id == team_ids[1] else team_ids[1])
            if self.fouls_to_give[defense_team_id] == 0:
                if isinstance(self, (Foul, FreeThrow, Rebound)):
                    if isinstance(self, Foul):
                        foul_event = self
                    elif isinstance(self, FreeThrow):
                        foul_event = self.foul_that_led_to_ft
                    else:
                        if not self.sub_type == 'offensive' and isinstance(self.missed_shot, FreeThrow):
                            foul_event = self.missed_shot.foul_that_led_to_ft
                        else:
                            return True
                    if not foul_event:
                        return True
                    fouls_to_give_prior_to_foul = foul_event.previous_event.fouls_to_give[defense_team_id]
                    if fouls_to_give_prior_to_foul > 0:
                        return False
                return True
        return False

    @property
    def counts_as_possession(self) -> bool:
        """
        returns True if event is possession changing event that should count as a real possession, False otherwise.
        Possessions that begin with less than 2 seconds left and have no point scored will not be counted.
        """
        if self.is_possession_ending_event:
            if self.seconds_remaining > 2:
                return True
            prev_event = self.previous_event
            while prev_event and not prev_event.is_possession_ending_event:
                prev_event = prev_event.previous_event
            if not prev_event or prev_event.seconds_remaining > 2:
                return True
            # possessions starts in final 2 seconds
            # return True if there is a FT or a FGM between now and end of period
            next_event = prev_event.next_event
            while next_event:
                if isinstance(next_event, FreeThrow) or \
                (isinstance(next_event, FieldGoal) and next_event.is_made):
                    return True
                next_event = next_event.next_event
        return False

    @property
    def lineup_ids(self) -> dict:
        """
        returns dict with lineup ids for each team for current event.
        Lineup ids are hyphen seperated sorted player id strings
        """
        lineup_ids = {}
        for team_id, team_players in self.players_on_court.items():
            players = sorted([player_id for player_id in team_players])
            lineup_id = "-".join(players)
            lineup_ids[team_id] = lineup_id
        return lineup_ids

    @property
    def base_stats(self) -> List[StatsModel]:
        """
        returns a list of StatsModel objects containing seconds played and possession count stats for event
        """
        return self._get_seconds_played_stats()

    def _get_seconds_played_stats(self) -> List[StatsModel]:
        """
        makes event StatsModel object for:
        - seconds played
        - second chance seconds played
        - over the limit seconds played
        """
        stat_models = []
        team_ids = list(self.players_on_court.keys())
        offense_team_id = self.offense_team_id
        is_over_the_limit = self.is_over_the_limit_event
        is_second_chance = self.is_second_chance_event
        if self.seconds_since_previous_event != 0:
            for team_id, players_ids in self.previous_event.players_on_court.items():
                seconds_stat_key = pbp.SECONDS_PLAYED_OFFENSE_STRING if team_id == offense_team_id else pbp.SECONDS_PLAYED_DEFENSE_STRING
                opponent_team_id = team_ids[0] if team_id == team_ids[1] else team_ids[1]
                previous_event_lineup_ids = self.previous_event.lineup_ids
                for player_id in players_ids:
                    keys = [seconds_stat_key]
                    if is_second_chance:
                        second_chance_seconds_stat_key = f'{pbp.SECOND_CHANCE_STRING}{seconds_stat_key}'
                        keys.append(second_chance_seconds_stat_key)
                    if is_over_the_limit:
                        over_the_limit_seconds_stat_key = f'{pbp.OVER_THE_LIMIT_STRING}{seconds_stat_key}'
                        keys.append(over_the_limit_seconds_stat_key)
                    for key in keys:
                        stat_model = StatsModel(
                            player_id=player_id,
                            team_id=team_id,
                            stat_key=key,
                            stat_value=self.seconds_since_previous_event,
                            opponent_team_id=opponent_team_id,
                            lineup_id=previous_event_lineup_ids[team_id],
                            opponent_lineup_id=previous_event_lineup_ids[opponent_team_id]
                        )
                        stat_models.append(stat_model)
        return stat_models

    def _add_lineup_data(self, stats_models: List[StatsModel]) -> List[StatsModel]:
        team_ids = list(self.players_on_court.keys())
        lineup_ids = self.lineup_ids
        for stats_model in stats_models:
            opponent_team_id = team_ids[0] if stats_model.team_id == team_ids[1] else team_ids[1]
            stats_model.lineup_id = lineup_ids[stats_model.team_id]
            stats_model.opponent_team_id = opponent_team_id
            stats_model.opponent_lineup_id = lineup_ids[opponent_team_id]
        return stats_models

    def _add_misc_stats(self, stat_key: str) -> List[str]:
        stat_keys = []
        if self.is_second_chance_event:
            stat_keys.append(f'{pbp.SECOND_CHANCE_STRING}{stat_key}')
        if self.is_over_the_limit_event:
            stat_keys.append(f'{pbp.OVER_THE_LIMIT_STRING}{stat_key}')
        return stat_keys

    @property
    def data(self):
        return self.__dict__
