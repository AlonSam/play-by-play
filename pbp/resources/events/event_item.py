from abc import ABCMeta, abstractmethod

import pbp.resources.events as e
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
    def players_on_court(self) -> list:
        """
        returns dict with list of player ids for each team with players on court for current event
        For all non substitution events on court players are just the same as previous event
        This function gets overwritten in events.substitution.Subsitutiton
        """
        return self.previous_event.players_on_court.copy()

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
    def is_penalty_event(self) -> bool:
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
    def data(self):
        return self.__dict__
