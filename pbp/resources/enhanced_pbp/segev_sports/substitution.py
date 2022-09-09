from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem
from pbp.resources.enhanced_pbp.substitution import Substitution


class SegevSubstitution(Substitution, SegevEnhancedPbpItem):
    """
    class for Substitution Events
    """
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def players_on_court(self):
        """
        returns dict with an updated list of player ids of each team
        """
        players = self.previous_event.players_on_court.copy()
        if hasattr(self, 'sub_out_player_id') and self.sub_out_player_id:
            players[self.team_id] = [self.sub_in_player_id if p == self.sub_out_player_id else p for p in players[self.team_id]]
        self.validate_lineup(players[self.team_id])
        return players

    def validate_lineup(self, players):
        if len(players) != 5:
            print(self)
            raise Exception('Lineup does not include 5 players')
        if len(players) != len(set(players)):
            raise Exception('Lineup has duplicates')