from pbp.resources.base import Base


class Boxscore(Base):
    """
    class for boxscore items

    : param list items: list of either:
        :obj SegevBoxScoreItem
        :obj FibaBoxScoreItem
        :obj ELBoxScoreItem
    """
    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        """
        returns dict with boxscore items split up by player and team
        """
        return {'player': self.player_items, 'team:': self.team_items}

    @property
    def player_items(self):
        """
        returns list of player boxscore items
        """
        return [item.data for item in self.items if hasattr(item, 'player_id')]

    @property
    def team_items(self):
        """
        returns list of team boxscore items
        """
        return [item.data for item in self.items if not hasattr(item, 'player_id')]

    @property
    def player_team_map(self):
        """
        returns dict mapping player id to team id
        """
        return {item['player_id']: item['team_id'] for item in self.player_items}


