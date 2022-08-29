import json
from time import time

from pymongo import MongoClient

from pbp.data_loader.possession_loader import PossessionLoader
from pbp.data_loader.segev_sports.enhanced_pbp.loader import SegevEnhancedPbpLoader
from pbp.objects.lineup import Lineup
from pbp.resources.possessions.possession import Possession


class SegevPossessionLoader(SegevEnhancedPbpLoader, PossessionLoader):
    client = MongoClient('localhost', 27017)
    db = client.PBP
    data_provider = 'segev_sports'
    resource = 'possessions'
    parent_object = 'Game'

    def __init__(self, game_id, source):
        super().__init__(game_id, source)
        self.events = self.items
        events_by_possession = self._split_events_by_possession()
        start_time = time()
        self.items = [Possession(**dict(events=possession_events)) for possession_events in events_by_possession]
        elapsed_time = time() - start_time
        print(f'Elapsed time to initialize Possessions: {elapsed_time}')
        start_time = time()
        self._add_extra_attrs_to_all_possessions()
        elapsed_time = time() - start_time
        print(f'Elapsed time to add attributes to all possessions: {elapsed_time}')
        start_time = time()
        self._save_data_to_db()
        elapsed_time = time() - start_time
        print(f'Elapsed time to save items to db: {elapsed_time}')

    @property
    def export_data(self):
        return [item.export_data for item in self.items]

    def _save_data_to_db(self):
        self._save_data_to_db_by_game()
        for item in self.items:
            self._save_data_to_db_by_team(item)
            self._save_data_to_db_by_player(item)
            self._save_data_to_db_by_lineup(item)

    def _save_data_to_db_by_game(self):
        col = self.db.games
        col.update_one({'_id': int(self.game_id)}, {'$set': {'possessions': self.export_data}}, upsert=True)

    def _save_data_to_db_by_team(self, item):
        col = self.db.teams
        offense_team_id = item.offense_team_id
        defense_team_id = item.defense_team_id
        col.update_one({'_id': offense_team_id}, {'$addToSet': {'possessions.offense': item.export_data}}, upsert=True)
        col.update_one({'_id': defense_team_id}, {'$addToSet': {'possessions.defense': item.export_data}}, upsert=True)

    def _save_data_to_db_by_player(self, item):
        col = self.db.players
        offense_lineup = item.offense_lineup_id.split('-')
        defense_lineup = item.defense_lineup_id.split('-')
        for player_id in offense_lineup:
            col.update_one({'_id': int(player_id)}, {'$addToSet': {'possessions.offense': item.export_data}},
                           upsert=True)
        for player_id in defense_lineup:
            col.update_one({'_id': int(player_id)}, {'$addToSet': {'possessions.defense': item.export_data}},
                           upsert=True)

    def _save_data_to_db_by_lineup(self, item):
        col = self.db.lineups
        names = ['offense', 'defense']
        for name in names:
            lineup = Lineup(id=getattr(item, f'{name}_lineup_id'), team_id=getattr(item, f'{name}_team_id'))
            col.update_one({'_id': lineup.id}, {'$addToSet': {'possessions.{name}': item.export_data,
                                                              'games': int(self.game_id)},
                                                '$set': {'player_ids': lineup.player_ids,
                                                         'team_id': lineup.team_id}},
                           upsert=True)

    def _save_data_to_file(self):
        with open('possessions.json', 'w') as outfile:
            json.dump(self.export_data, outfile, indent=4)
