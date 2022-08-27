from pprint import pprint

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
        self.source_data = self.source.load_data(self.game_id)
        self._make_boxscore_items()
        self._save_data_to_db()
        self.client.close()

    def _make_boxscore_items(self):
        self.items = [SegevBoxScoreItem(**item) for item in self.source_data]

    @classmethod
    def from_web(cls, game_id):
        return cls(game_id, SegevBoxScoreWebLoader())

    @classmethod
    def from_db(cls, game_id):
        return cls(game_id, SegevBoxScoreDBLoader())

    def _save_data_to_db(self):
        self._save_data_by_game()
        for item in self.items:
            self._save_data_by_team(item)
            if hasattr(item, 'player_id') and item.player_id != 0:
                self._save_data_by_player(item)
        self.client.close()

    def _save_data_by_game(self):
        col = self.db.games
        col.update_one({'_id': int(self.game_id)}, {'$set': {'boxscore': self.data}}, upsert=True)

    def _save_data_by_team(self, item):
        col = self.db.teams
        query = {'_id': item.team_id}
        col.update_one(query, {'$addToSet': {'boxscores': item.dict()}}, upsert=True)

    def _save_data_by_player(self, item):
        col = self.db.players
        query = {'_id': item.player_id}
        col.update_one(query, {'$addToSet': {'boxscores': item.dict()}}, upsert=True)

    @property
    def data(self):
        return [item.dict() for item in self.items]


box_score_loader = SegevBoxScoreLoader.from_web('51957')
pprint(box_score_loader.data)