import math

import pbp


class FieldGoal(object):
    """
    Class for field goal events
    """
    event_type = ['2pt', '3pt']

    @property
    def is_blocked(self):
        """
        returns True is shot was blocked, False otherwise
        """
        pass

    @property
    def is_assisted(self):
        """
        returns True is shot was assisted, False otherwise
        """
        pass

    @property
    def rebound(self):
        """
        returns True is shot was rebounded, False otherwise
        """
        pass

    @property
    def is_heave(self):
        """
        returns True is shot was a last second heave, False otherwise
        """
        pass

    @property
    def is_corner_3(self):
        """
        returns True is shot was a corner 3, False otherwise
        """
        pass

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
        if not prev_ev:
            return False
        if not hasattr(prev_ev, "is_real_rebound"):
            return False
        if not prev_ev.is_real_rebound:
            return False
        in_time = prev_ev.seconds_remaining - self.seconds_remaining <= 2
        return prev_ev.sub_type == 'offensive' and prev_ev.player == self.player and in_time


    @property
    def shot_data(self):
        """
        returns a dict with detailed shot data
        """
        team_ids = list(self.players_on_court.keys())
        opponent_team_id = team_ids[0] if self.team_id == team_ids[1] else team_ids[1]
        shot_data = {
            "PlayerId": self.player_id,
            "TeamId": self.team_id,
            "OpponentTeamId": opponent_team_id,
            "LineupId": self.lineup_ids[self.team_id],
            "OpponentLineupId": self.lineup_ids[opponent_team_id],
            "Made": self.is_made,
            "X": self.x if hasattr(self, "x") else None,
            "Y": self.y if hasattr(self, "y") else None,
            "Time": self.seconds_remaining,
            "ShotValue": self.shot_value,
            "Putback": self.is_putback,
            "ShotType": self.shot_type,
            "ScoreMargin": self.margin,
            "EventId": self.event_id,
            "IsAnd1": self.is_and_one,
        }
        if self.is_made:
            shot_data["Assisted"] = self.is_assisted
            if self.is_assisted:
                shot_data["AssistPlayerId"] = self.assist_player_id
        if not self.is_made:
            shot_data["Blocked"] = self.is_blocked
            if self.is_blocked:
                shot_data["BlockPlayerId"] = self.block_player_id
        if self.is_second_chance_event:
            prev_event = self.previous_event
            while not (prev_event.event_type == 'rebound' and prev_event.is_offensive):
                prev_event = prev_event.previous_event
            shot_data["SecondsSinceOReb"] = prev_event.seconds_remaining - self.seconds_remaining
            shot_data["OrebShotPlayerId"] = prev_event.missed_shot.player_id
            shot_data["OrebReboundPlayerId"] = prev_event.player_id
            if prev_event.player_id != 0:
                if isinstance(prev_event.missed_shot, FieldGoal):
                    rebound_shot_type = prev_event.missed_shot.shot_type
                    if prev_event.missed_shot.is_blocked:
                        rebound_shot_type += pbp.BLOCKED_STRING
                else:
                    rebound_shot_type = 'FreeThrow'
            else:
                rebound_shot_type = "Team"
            shot_data["OrebShotType"] = rebound_shot_type
        return shot_data
