import pbp.resources.events as e
from pbp.resources.events import Rebound, Foul, FieldGoal
from pbp.resources.events.segev_sports.event_item import SegevEventItem


class SegevFieldGoal(FieldGoal, SegevEventItem):
    """
    class for Field Goal Events
    """
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return f'{"made" if self.is_made else "missed"} {self.action_type} {self.sub_type} by {self.player_id}' \
               f'at period {self.period} and {self.time} left to play'

    @property
    def is_blocked(self) -> bool:
        """
        returns True if shot was blocked
        """
        return not self.is_made and hasattr(self, e.BLOCK_ID_STRING)

    @property
    def is_assisted(self) -> bool:
        """
        returns True if shot was assisted, False otherwise
        """
        return self.is_made and hasattr(self, e.ASSIST_ID_STRING)

    @property
    def is_putback(self) -> bool:
        """
        returns True if shot is a 2pt attempt within 2 seconds of an
        offensive rebound attempted by the same player who got the rebound
        """
        if self.is_assisted or self.shot_value == 3:
            return False
        prev_ev = self.previous_event
        while prev_ev and not (isinstance(prev_ev, Rebound) and prev_ev.is_offensive):
            prev_ev = prev_ev.previous_event
        if not prev_ev:
            return False
        in_time = prev_ev.seconds_remaining - self.seconds_remaining <= 2
        return prev_ev.sub_type == e.OFFENSIVE_STRING and prev_ev.player_id == self.player_id and in_time

    @property
    def is_and_one(self) -> bool:
        """
        returns True if the shooter was fouled during the shot, False otherwise
        """
        if self.is_make_that_does_not_end_possession:
            return isinstance(self.next_event, Foul) and self.next_event.is_and_one_foul
        return False

    def get_offense_team_id(self) -> str:
        """
        returns team id that took the shot
        """
        return self.team_id