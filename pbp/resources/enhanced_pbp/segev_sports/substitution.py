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
        if hasattr(self, 'sub_out_player_id'):
            players[self.team_id] = [self.sub_in_player_id if p == self.sub_out_player_id else p for p in players[self.team_id]]
        return players

    @property
    def export_data(self):
        team_ids = list(self.players_on_court.keys())
        opponent_team_id = team_ids[0] if self.team_id == team_ids[1] else team_ids[1]
        data = {
            'team_id': self.team_id,
            'opponent_team_id': opponent_team_id,
            'lineup_id': self.lineup_ids[self.team_id],
            'opponent_lineup_id': self.lineup_ids[opponent_team_id],
            'quarter': self.period,
            'score': self.score,
            'score_margin': self.margin,
            'time': self.time,
            'seconds_remaining': self.seconds_remaining,
            'seconds_since_previous_event': self.seconds_since_previous_event,
            'fouls_to_give': self.fouls_to_give,
            'player_game_fouls': self.player_game_fouls,
            'is_penalty_event': self.is_penalty_event,
            'is_second_chance_event': self.is_second_chance_event,
            'action_type': 'Substitution',
            'sub_in_player_id': self.sub_in_player_id,
            'sub_out_player_id': self.sub_out_player_id if hasattr(self, 'sub_out_player_id') else None
        }
        return data