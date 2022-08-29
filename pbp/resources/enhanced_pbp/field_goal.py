import pbp


class FieldGoal(object):
    """
    Class for field goal events
    """
    event_type = ['2pt', '3pt']

    @property
    def rebound(self):
        """
        returns True is shot was rebounded, False otherwise
        """
        pass

    @property
    def is_corner_3(self):
        """
        returns True is shot was a corner 3, False otherwise
        """
        pass

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
