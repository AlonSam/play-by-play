import math

import pbp
from pbp.resources.enhanced_pbp import Foul, Rebound
from pbp.resources.enhanced_pbp.field_goal import FieldGoal
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem


class SegevFieldGoal(FieldGoal, SegevEnhancedPbpItem):
    """
    class for Field Goal Events
    """
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def is_blocked(self):
        """
        returns True is shot was blocked, False otherwise
        """
        return not self.is_made and hasattr(self, 'block_player_id')

    @property
    def is_assisted(self):
        """
        returns True is shot was assisted, False otherwise
        """
        return self.is_made and hasattr(self, 'assist_player_id')

    @property
    def rebound(self):
        """
        returns
        """
        if not self.is_made and isinstance(self.next_event, Rebound):
            return self.next_event
        return None

    @property
    def is_heave(self):
        """
        returns True is shot was a last second heave, False otherwise
        """
        return self.distance > pbp.HEAVE_DISTANCE_CUTOFF and self.seconds_remaining < pbp.HEAVE_TIME_CUTOFF

    @property
    def is_corner_3(self):
        """
        returns True is shot was a corner 3, False otherwise
        """
        return self.shot_value == 3 and self.x <= 11

    @property
    def distance(self):
        """
        returns shot distance
        """
        if hasattr(self, 'x') and hasattr(self, 'y'):
            x_squared = ((self.x - 5) * 2) ** 2
            y_squared = (self.y - 50) ** 2
            shot_distance = math.sqrt(x_squared + y_squared)
            return round(shot_distance, 1)

    @property
    def shot_type(self):
        """
        returns shot type string ('AtRim', 'ShortMidRange', 'LongMidRange', 'Arc3' or 'Corner3')
        """
        if self.shot_value == 3:
            if self.is_corner_3:
                return pbp.CORNER_3_STRING
            else:
                return pbp.ARC_3_STRING
        if self.distance:
            if self.distance < pbp.AT_RIM_CUTOFF:
                return pbp.AT_RIM_STRING
            elif self.distance < pbp.SHORT_MID_RANGE_CUTOFF:
                return pbp.SHORT_MID_RANGE_STRING
            else:
                return pbp.LONG_MID_RANGE_STRING
        return pbp.UNKNOWN_SHOT_DISTANCE_STRING

    @property
    def is_putback(self):
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
        return prev_ev.sub_type == 'offensive' and prev_ev.player_id == self.player_id and in_time

    @property
    def is_and_one(self):
        if self.is_make_that_does_not_end_possession:
            return isinstance(self.next_event, Foul) and self.next_event.is_and_one_foul
        return False

    @property
    def is_make_that_does_not_end_possession(self):
        return self.is_made and not self.is_possession_ending_event

    def get_offense_team_id(self):
        """
        returns team id that took the shot
        """
        return self.team_id

    @property
    def export_data(self):
        data = {
            'action_type': 'FieldGoal',
            'is_made': self.is_made,
            'x': self.x,
            'y': self.y,
            'shot_distance': self.distance,
            'shot_value': self.shot_value,
            'shot_area': self.shot_type,
            'shot_type': self.sub_type,
            'is_putback': self.is_putback,
            'is_and1': self.is_and_one,
            'is_blocked': self.is_blocked,
            'block_player_id': self.block_player_id if self.is_blocked else 0,
            'is_assisted': self.is_assisted,
            'assist_player_id': self.assist_player_id if self.is_assisted else 0,
            'rebound_player_id': self.rebound.player_id if self.rebound else 0,
        }
        base_data = self.base_data.copy()
        base_data.update(data)
        return base_data
