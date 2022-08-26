from pymongo import MongoClient

from pbp.data_loader.segev_sports.boxscore.db import SegevBoxScoreDBLoader
from pbp.data_loader.segev_sports.boxscore.web import SegevBoxScoreWebLoader
from pbp.resources.boxscore.segev_boxscore_item import SegevBoxScoreItem


class SegevBoxScoreLoader(object):
    """
        Loads segev_sports pbp data for game
        :param str game_id: segev_sports Game ID
        :param str source: Where the data should be loaded from - db or web
        :param lst competition: List that contains the name of competition, season and phase in season.
        """
    client = MongoClient('localhost', 27017)
    db = client.PBP
    data_provider = 'segev_sports'
    resource = 'boxscore'
    parent_object = 'Game'

    def __init__(self, game_id, source):
        self.game_id = game_id
        self.source = source
        self.source_data = self.load_data()
        self._make_boxscore_items()
        self._save_data_to_db()
        self.client.close()

    def load_data(self):
        if self.source == 'web':
            source_loader = SegevBoxScoreWebLoader()
        else:
            source_loader = SegevBoxScoreDBLoader()
        return source_loader.load_data(self.game_id)

    def _make_boxscore_items(self):
        if 'result' in self.source_data:
            self.source_data = self.source_data['result']['boxscore']
            home_id = self.source_data['gameInfo']['homeTeamId']
            away_id = self.source_data['gameInfo']['awayTeamId']
            home = self.source_data['homeTeam']
            away = self.source_data['awayTeam']
            self.items = [SegevBoxScoreItem(item, self.game_id, home_id) for item in home['players']]
            self.items += [SegevBoxScoreItem(item, self.game_id, away_id) for item in away['players']]
            home['teamActions'].update(self.source_data['gameInfo']['homeGameStats'])
            away['teamActions'].update(self.source_data['gameInfo']['awayGameStats'])
            self.items.append(SegevBoxScoreItem(home['teamActions'], self.game_id, home_id))
            self.items.append(SegevBoxScoreItem(away['teamActions'], self.game_id, away_id))
        else:
            self.items = [SegevBoxScoreItem(item, self.game_id) for item in self.source_data]

    def _save_data_to_db(self):
        self._save_data_by_game()
        for item in self.items:
            self._save_data_by_team(item)
            if hasattr(item, 'player_id'):
                self._save_data_by_player(item)
        self.client.close()

    def _save_data_by_game(self):
        col = self.db.games
        col.update_one({'_id': int(self.game_id)}, {'$set': {'boxscore': self.data}}, upsert=True)

    def _save_data_by_team(self, item):
        col = self.db.teams
        query = {'_id': item.team_id}
        col.update_one(query, {'$addToSet': {'boxscores': item.data}}, upsert=True)

    def _save_data_by_player(self, item):
        col = self.db.players
        query = {'_id': item.player_id}
        col.update_one(query, {'$addToSet': {'boxscores': item.data}}, upsert=True)

    @property
    def data(self):
        return [item.data for item in self.items]