from typing import List

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from pbp.data_loader import SegevPossessionLoader, SegevDetailsLoader
from pbp.data_loader.segev_sports.boxscore.loader import SegevBoxScoreLoader
from pbp.data_loader.segev_sports.enhanced_pbp.loader import SegevEnhancedPbpLoader
from pbp.data_loader.segev_sports.pbp.loader import SegevPbpLoader
from pbp.models.possession import Possession
from pbp.objects.game import Game
from pbp.objects.lineup import Lineup
from pbp.objects.team import Team
from pbp.resources.boxscore.segev_boxscore_item import SegevBoxScoreItem
from pbp.resources.details.segev_details_item import SegevDetailsItem


class Client(object):
    def __init__(self, basket_id):
        self.basket_id = basket_id

    def load_details(self) -> SegevDetailsItem:
        details_loader = SegevDetailsLoader(self.basket_id)
        details = details_loader.item
        self.game_id = details.game_id
        self.players = details_loader.players
        return details

    def load_boxscore(self) -> List[SegevBoxScoreItem]:
        boxscore_loader = SegevBoxScoreLoader(self.game_id)
        return boxscore_loader.items

    def load_possessions(self) -> List[Possession]:
        pbp_loader = SegevPbpLoader(self.game_id)
        raw_events = pbp_loader.items
        enhanced_pbp_loader = SegevEnhancedPbpLoader(self.game_id, raw_events, self.details.home_id,
                                                     self.details.away_id)
        events = enhanced_pbp_loader.events
        possession_loader = SegevPossessionLoader(events)
        return possession_loader.possessions

    def load_game(self):
        self.details = self.load_details()
        self.boxscore = self.load_boxscore()
        self.possessions = self.load_possessions()
        self.possession_ids = [possession.possession_id for possession in self.possessions]
        self.game = Game(game_id=self.game_id, basket_id=self.basket_id,
                    details=self.details, boxscore=self.boxscore, possessions=self.possession_ids)
        self._save_data_to_db()

    def _save_data_to_db(self):
        mongo_client = MongoClient('localhost', 27017)
        self.db = mongo_client.PBP
        self._save_game_to_db()
        self._save_teams_to_db()
        self._save_players_to_db()
        for possession in self.possessions:
            self._save_possession_to_db(possession)
            self._save_possession_to_db_by_team(possession)
            self._save_possession_to_db_by_player(possession)
            self._save_data_to_db_by_lineup(possession)
        mongo_client.close()

    def _save_possession_to_db(self, possession: Possession):
        col = self.db.possessions
        possession_dict = possession.dict(by_alias=True, exclude_none=True)
        try:
            col.insert_one(possession_dict)
        except DuplicateKeyError:
            return

    def _save_game_to_db(self):
        col = self.db.games
        col.update_one({'_id': self.game_id}, {'$set': self.game.dict(by_alias=True)}, upsert=True)

    def _save_teams_to_db(self):
        col = self.db.teams
        names = ['home', 'away']
        for name in names:
            team_id = getattr(self.details, f'{name}_id')
            boxscores = [b.data for b in self.boxscore if b.team_id == team_id]
            query = {'_id': team_id}
            team_dict = col.find_one(query)
            if team_dict:
                col.update_one(query, {'$addToSet': {'games': self.game_id},
                                       '$push': {'boxscores': {'$each': boxscores}}})
            else:
                team_name = getattr(self.details, f'{name}_team')
                team = Team(id=team_id, name=team_name, boxscores=boxscores, games=[self.game_id])
                col.insert_one(team.data)

    def _save_players_to_db(self):
        col = self.db.players
        for player in self.players:
            player_id = player.id
            boxscore = [b.data for b in self.boxscore if b.player_id == player_id]
            query = {'_id': player_id}
            player_dict = col.find_one(query)
            if player_dict:
                col.update_one(query, {'$addToSet': {'games': self.game_id},
                                       '$push': {'boxscores': {'$each': boxscore}}})
            else:
                player.boxscores += boxscore
                player.games.append(self.game_id)
                col.insert_one(player.data)

    def _save_possession_to_db_by_team(self, possession: Possession):
        col = self.db.teams
        names = ['offense', 'defense']
        for name in names:
            team_id = getattr(possession, f'{name}_team_id')
            query = {'_id': team_id}
            col.update_one(query, {'$push': {f'possessions.{name}': possession.possession_id}})

    def _save_possession_to_db_by_player(self, possession: Possession):
        col = self.db.players
        names = ['offense', 'defense']
        for name in names:
            lineup = Lineup(id=getattr(possession, f'{name}_lineup_id'), team_id=getattr(possession, f'{name}_team_id'))
            for player_id in lineup.player_ids:
                query = {'_id': player_id}
                col.update_one(query, {'$push': {f'possessions.{name}': possession.possession_id}})

    def _save_data_to_db_by_lineup(self, possession: Possession):
        col = self.db.lineups
        names = ['offense', 'defense']
        for name in names:
            lineup_id = getattr(possession, f'{name}_lineup_id')
            query = {'_id': lineup_id}
            lineup_dict = col.find_one(query)
            if lineup_dict:
                lineup = Lineup(**lineup_dict)
                if self.game_id not in lineup.games:
                    lineup.games.append(self.game_id)
            else:
                lineup = Lineup(id=lineup_id, team_id=getattr(possession, f'{name}_team_id'))
                lineup.games.append(self.game_id)
            if name not in lineup.possessions.keys():
                lineup.possessions[name] = []
            lineup.possessions[name].append(possession.possession_id)
            col.update_one(query, {'$set': lineup.data}, upsert=True)

    def get_team_name(self, team_id):
        if team_id == self.details.home_id:
            return self.details.home_team
        return self.details.away_team

    def get_player(self, player_id):
        for player in self.players:
            if player.id == player_id:
                return player


# for game_id in range(24483, 24500):
#     client = Client(str(game_id))
#     client.load_game()

client = Client('24486')
client.load_game()