from pymongo import MongoClient

from pbp.data_loader.segev_sports.details.db import SegevDetailsDBLoader
from pbp.data_loader.segev_sports.details.web import SegevDetailsWebLoader
from pbp.data_loader.segev_sports.web_loader import SegevWebLoader
from pbp.resources.games.segev_game_item import SegevGameItem
from pbp.resources.teams.segev_team_item import SegevTeamItem


class SegevDetailsLoader(object):
    """
        Loads segev_sports pbp data for game
        :param str game_id: segev_sports Game ID
        :param str source: Where the data should be loaded from - db or web
        """
    client = MongoClient('localhost', 27017)
    db = client.PBP
    data_provider = 'segev_sports'
    resource = 'details'
    parent_object = 'Game'

    def __init__(self, source: SegevWebLoader, game_id=None, basket_id=None):
        self.source = source
        self.game_id = game_id
        self.basket_id = basket_id
        self._load_data()

    def _load_data(self):
        if self.basket_id:
            self.source_data, self.players = self.source.load_data(self.basket_id)
            self.game_id = str(self.source_data['game_id'])
            self._make_game_item()
            self._save_data_to_db()
        else:
            self.source_data = self.source.load_data(self.game_id)
            self.basket_id = str(self.source_data['basket_id'])
            self._make_game_item()

    @classmethod
    def from_web(cls, game_id):
        return cls(SegevDetailsWebLoader(), basket_id=game_id)

    @classmethod
    def from_db(cls, game_id):
        return cls(SegevDetailsDBLoader(), game_id=game_id)

    def _save_data_to_db(self):
        self._save_game_to_db()
        self._save_teams_to_db()
        self._save_players_to_db()

    def _save_game_to_db(self):
        col = self.db.games
        col.update_one({'_id': int(self.game_id), 'basketId': int(self.basket_id)},
                       {'$set': {'details': self.data}}, upsert=True)

    def _save_teams_to_db(self):
        names = ['home', 'away']
        teams = [SegevTeamItem(self.data[f'{name}_id'], self.data[f'{name}_team'], self.data['competition']) for name in names]
        col = self.db.teams
        for team in teams:
            col.update_one({'_id': team.id}, {'$set': {'name': team.name, 'competitions': team.competitions},
                                              '$addToSet': {'games': int(self.game_id)}}, upsert=True)

    def _save_players_to_db(self):
        names = ['home', 'away']
        col = self.db.players
        for player in self.players:
            col.update_one({'_id': player.id}, {'$set': {'name': player.name, 'hebrewName': player.hebrew_name,
                                                         'teamId': player.team_id, 'shirtNumber': player.shirt_number},
                                                '$addToSet': {'games': int(self.game_id)}}, upsert=True)

    def _make_game_item(self):
        self.item = SegevGameItem(**self.source_data)

    @property
    def data(self):
        return self.item.dict()