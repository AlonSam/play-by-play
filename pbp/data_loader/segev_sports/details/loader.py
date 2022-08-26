from pymongo import MongoClient

from pbp.data_loader.segev_sports.details.db import SegevDetailsDBLoader
from pbp.data_loader.segev_sports.details.web import SegevDetailsWebLoader
from pbp.resources.games.segev_game_item import SegevGameItem
from pbp.resources.players.segev_player_item import SegevPlayerItem
from pbp.resources.teams.segev_team_item import SegevTeamItem


class DataCannotBeLoadedException(Exception):
    """
    Class for exception when trying to load data from database without game_id or when trying to load data
    from web without basket_id
    """


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

    def __init__(self, source, game_id=None, basket_id=None):
        self.source = source
        if self.source == 'db':
            if game_id:
                self.game_id = game_id
                self.load_data_from_db()
            else:
                raise DataCannotBeLoadedException('Cannot load data from database without game_id')
        elif basket_id:
            self.basket_id = basket_id
            self.load_data_from_web()
        else:
            raise DataCannotBeLoadedException('Cannot load data from web without basket_id')

    def load_data_from_db(self):
        source_loader = SegevDetailsDBLoader()
        self.source_data = source_loader.load_data(self.game_id)
        self._make_game_item()

    def load_data_from_web(self):
        self.basket_data = self.load_basket_data()
        self.game_id = str(self.basket_data['game_id'])
        source_loader = SegevDetailsWebLoader()
        self.source_data = source_loader.load_data(self.game_id)
        self._save_players_to_db()
        self._make_game_item()
        self._save_teams_to_db()
        self._save_data_to_db()

    def load_basket_data(self):
        if self.source == 'web':
            source_loader = SegevDetailsWebLoader()
        else:
            source_loader = SegevDetailsDBLoader()
        return source_loader.load_basket_data(self.basket_id)

    def _save_data_to_db(self):
        col = self.db.games
        col.update_one({'_id': int(self.game_id), 'basket_id': int(self.basket_id)},
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
        self.players = []
        for name in names:
            raw_players = self.source_data[f'{name}Team']['players']
            self.players += [SegevPlayerItem(player, self.source_data[f'{name}Team']['id']) for player in raw_players]
        col = self.db.players
        for player in self.players:
            col.update_one({'_id': player.id}, {'$set': {'name': player.name, 'hebrew_name': player.hebrew_name,
                                                         'team_id': player.team_id, 'shirt_number': player.shirt_number},
                                                '$addToSet': {'games': int(self.game_id)}}, upsert=True)

    def _make_game_item(self):
        if hasattr(self, 'basket_data'):
            self.item = SegevGameItem(self.source_data, self.basket_data)
        else:
            self.item = SegevGameItem(self.source_data)

    @property
    def data(self):
        return self.item.data


# game_id = '51959'
# pbp_loader = SegevDetailLoader('web', basket_id='24484')