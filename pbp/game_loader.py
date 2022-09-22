from __future__ import annotations

from pymongo import MongoClient

from pbp.data_loader import SegevPossessionLoader, SegevDetailsLoader
from pbp.data_loader.segev_sports.boxscore_loader import SegevBoxScoreLoader
from pbp.data_loader.segev_sports.event_loader import SegevEventLoader
from pbp.data_loader.segev_sports.pbp_loader import SegevPbpLoader
from pbp.models.db import *


class GameLoader:
    def __init__(self, basket_id) -> None:
        self.basket_id = basket_id

    def load_details(self) -> DetailsModel:
        details_loader = SegevDetailsLoader(self.basket_id)
        details = details_loader.item
        self.game_id = details.game_id
        self.players = details_loader.players
        return details

    def load_boxscore(self) -> list[BoxScoreModel]:
        boxscore_loader = SegevBoxScoreLoader(self.game_id)
        return boxscore_loader.items

    def load_possessions(self) -> list[PossessionModel]:
        pbp_loader = SegevPbpLoader(self.game_id)
        raw_events = pbp_loader.items
        enhanced_pbp_loader = SegevEventLoader(self.game_id, raw_events, self.details.home_id,
                                               self.details.away_id)
        events = enhanced_pbp_loader.events
        possession_loader = SegevPossessionLoader(events, self.details.home_id, self.details.away_id)
        return possession_loader.possessions

    def load_game(self) -> None:
        self.details = self.load_details()
        self.boxscore = self.load_boxscore()
        self.possessions = self.load_possessions()
        possession_ids = [possession.possession_id for possession in self.possessions]
        self.game = GameModel(id=self.game_id, basket_id=self.basket_id,
                    details=self.details, boxscore=self.boxscore, possessions=possession_ids)
        self._save_data_to_db()

    def _save_data_to_db(self) -> None:
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

    def _save_possession_to_db(self, possession: PossessionModel) -> None:
        col = self.db.possessions
        possession_dict = possession.data
        col.update_one({'_id': possession.possession_id}, {'$set': possession_dict}, upsert=True)

    def _save_game_to_db(self) -> None:
        col = self.db.games
        col.update_one({'_id': self.game_id}, {'$set': self.game.dict(by_alias=True, exclude_none=True)}, upsert=True)

    def _save_teams_to_db(self) -> None:
        col = self.db.teams
        names = ['home', 'away']
        for name in names:
            team_id = getattr(self.details, f'{name}_id')
            boxscores = [b.data for b in self.boxscore if b.team_id == team_id]
            query = {'_id': team_id}
            team_dict = col.find_one(query)
            if team_dict:
                col.update_one(query, {'$addToSet': {'games': self.game_id,
                                                     'seasons': self.details.season},
                                       '$push': {'boxscores': {'$each': boxscores}}})
            else:
                team_name = getattr(self.details, f'{name}_team')
                team = TeamModel(id=team_id, name=team_name, boxscores=boxscores,
                                 games=[self.game_id], seasons=[self.details.season])
                col.insert_one(team.data)

    def _save_players_to_db(self) -> None:
        col = self.db.players
        for player in self.players:
            player_id = player.id
            boxscore = [b.data for b in self.boxscore if b.player_id == player_id]
            query = {'_id': player_id}
            player_dict = col.find_one(query)
            if player_dict:
                col.update_one(query, {'$addToSet': {'games': self.game_id},
                                       '$push': {'boxscores': {'$each': boxscore}},
                                       '$set': {f'teamIds.{self.details.season}': player.team_id,
                                                'teamId': player.team_id}
                                       }
                               )
            else:
                player.boxscores += boxscore
                player.games.append(self.game_id)
                col.insert_one(player.data)

    def _save_possession_to_db_by_team(self, possession: PossessionModel) -> None:
        col = self.db.teams
        names = ['offense', 'defense']
        for name in names:
            team_id = getattr(possession, f'{name}_team_id')
            query = {'_id': team_id}
            col.update_one(query, {'$push': {f'possessions.{name}': possession.possession_id}})

    def _save_possession_to_db_by_player(self, possession: PossessionModel) -> None:
        col = self.db.players
        names = ['offense', 'defense']
        for name in names:
            lineup = LineupModel(id=getattr(possession, f'{name}_lineup_id'), team_id=getattr(possession, f'{name}_team_id'))
            for player_id in lineup.player_ids:
                query = {'_id': player_id}
                col.update_one(query, {'$push': {f'possessions.{name}': possession.possession_id}})

    def _save_data_to_db_by_lineup(self, possession: PossessionModel) -> None:
        col = self.db.lineups
        names = ['offense', 'defense']
        for name in names:
            lineup_id = getattr(possession, f'{name}_lineup_id')
            query = {'_id': lineup_id}
            lineup_dict = col.find_one(query)
            if lineup_dict:
                lineup = LineupModel(**lineup_dict)
                if self.game_id not in lineup.games:
                    lineup.games.append(self.game_id)
            else:
                lineup = LineupModel(id=lineup_id, team_id=getattr(possession, f'{name}_team_id'))
                lineup.games.append(self.game_id)
            if name not in lineup.possessions.keys():
                lineup.possessions[name] = []
            lineup.possessions[name].append(possession.possession_id)
            col.update_one(query, {'$set': lineup.data}, upsert=True)

    def get_team_name(self, team_id: str) -> str:
        if team_id == self.details.home_id:
            return self.details.home_team
        return self.details.away_team

    def get_player(self, player_id: str) -> PlayerModel:
        for player in self.players:
            if player.id == player_id:
                return player