from pbp.resources.enhanced_pbp import StartOfPeriod, Substitution
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem

class InvalidNumberOfStartersException(Exception):
    """
    Class for exception when a team's 5 period starters can't be determined.
    You can add the correct period starters to
    overrides/missing_period_starters.json in your data directory to fix this.
    """

    pass


class SegevStartOfPeriod(StartOfPeriod, SegevEnhancedPbpItem):
    """
    class for Start Of Period Events
    """

    @property
    def players_on_court(self):
        """
        returns period starters
        """
        return self.period_starters

    def get_period_starters(self):
        try:
            return self.get_period_starters_from_events()
        except InvalidNumberOfStartersException:
            return self.get_period_starters_from_boxscore()

    def get_period_starters_from_events(self):
        if self.period == 1:
            starters = {}
        else:
            starters = self.previous_event.players_on_court
        event = self.next_event
        while isinstance(event, Substitution):
            if event.team_id not in starters.keys():
                starters[event.team_id] = list()
            if hasattr(event, 'sub_out_player_id') and event.sub_out_player_id\
                    and event.sub_out_player_id in starters[event.team_id]:
                starters[event.team_id].remove(event.sub_out_player_id)
            starters[event.team_id].append(event.sub_in_player_id)
            event = event.next_event
        self._validate_5_starters(starters)
        return starters

    def get_period_starters_from_boxscore(self):
        pass

    def _validate_5_starters(self, starters):
        for team_id, team_starters in starters.items():
            if len(team_starters) != 5:
                raise InvalidNumberOfStartersException(f"GameId: {self.game_id}, Period: {self.period}, TeamId: {team_id}, Players: {team_starters})")

    @property
    def export_data(self):
        data = self.dict(by_alias=True, exclude_none=True, exclude={'previous_event', 'next_event', 'period_starters'})
        data.update(self.base_data)
        return data
