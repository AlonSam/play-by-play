from pbp.resources.events.segev_sports.event_item import SegevEventItem
from pbp.resources.events.substitution import Substitution


class SegevSubstitution(Substitution, SegevEventItem):
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

    def validate_lineup(self, players) -> None:
        """
        :param players: List of player_ids
        validates that the lineup includes exactly 5 players without duplicates. Raises Exceptions otherwise.
        """
        if len(players) != 5:
            print(f'game_id: {self.game_id}, period: {self.period}, time: {self.time}, lineup: {players}')
            raise Exception('Lineup does not include 5 players')
        if len(players) != len(set(players)):
            print(f'game_id: {self.game_id}, period: {self.period}, time: {self.time}, lineup: {players}')
            raise Exception('Lineup has duplicates')