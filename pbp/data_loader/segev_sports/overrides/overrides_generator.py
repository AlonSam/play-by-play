class OverridesGenerator:
    def __init__(self, event_id, team_id, period, time, player_id=None):
        self.event_id = event_id
        self.team_id = team_id
        self.period = period
        self.time = time
        self.player_id = player_id

    def generate_event(self):
        return {
            'quarter': self.period,
            'id': self.event_id,
            'parentActionId': 0,
            'userTime': '18:15:15',
            'quarterTime': self.time,
            'playerId': self.player_id,
            'teamId': self.team_id
        }

    def generate_sub(self, player_in, player_out):
        sub_in = self.generate_sub_in(player_in)
        sub_out = self.generate_sub_out(player_out)
        return [sub_in, sub_out]


    def generate_sub_in(self, player_in):
        event = self.generate_event()
        event.update({
            'type': 'substitution',
            'playerId': player_in,
            'parameters': {
                'playerIn': "1",
                'playerOut': None
            }
        })
        return event

    def generate_sub_out(self, player_out):
        event = self.generate_event()
        event.update({
            'type': 'substitution',
            'id': str(int(self.event_id) + 1),
            'playerId': player_out,
            'parameters': {
                'playerIn': None,
                'playerOut': "1"
            }
        })
        return event

    def generate_shot(self, shot_type, x, y, made, pts, fb, sc, to, score=None):
        event = self.generate_event()
        event.update({
            'type': 'shot',
            'score': score,
            'parameters': {
                'team': 1,
                'player': "1",
                'coordX': x,
                'coordY': y,
                'points': pts,
                'type': shot_type,
                'fastBreak': fb,
                'secondChancePoints': sc,
                'pointsFromTurnover': to,
                'made': made
            }
        })
        return event

    def generate_rebound(self, type):
        event = self.generate_event()
        event.update({
            'type': 'rebound',
            'parameters': {
                'team': 1,
                'player': '1',
                'type': type
            }
        })
        return event

    def generate_foul(self, foul_type, kind, free_throws):
        event = self.generate_event()
        event.update({
            'type': 'foul',
            'parameters': {
                'team': 1,
                'player': '1',
                'type': foul_type,
                'kind': kind,
                'fouledOn': "1",
                'freeThrows': free_throws
            }
        })
        return event

    def generate_foul_on(self):
        event = self.generate_event()
        event.update({
            'type': 'foul-drawn',
            'parameters': {
                'team': 1,
                'player': "1"
            }
        })
        return event

    def generate_free_throw(self, made, ft_number, ft_awarded, fb, sc, to, score=None):
        event = self.generate_event()
        event.update({
            'type': 'freeThrow',
            'score': score,
            'parameters': {
                'team': 1,
                'player': "1",
                'made': made,
                'freeThrowsAwarded': ft_awarded,
                'freeThrowNumber': ft_number,
                'fastBreak': fb,
                'secondChancePoints': sc,
                'pointsFromTurnover': to
            }
        })
        return event

    def generate_turnover(self, type):
        event = self.generate_event()
        event.update({
            'type': 'turnover',
            'parameters': {
                'team': 1,
                'player': "1",
                'type': type
            }
        })
        return event

    def generate_steal(self):
        event = self.generate_event()
        event.update({
            'type': 'steal',
            'parameters': {
                'team': 1,
                'player': "1"
            }
        })
        return event

