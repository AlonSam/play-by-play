import json

from pymongo import MongoClient

from pbp.data_loader.possession_loader import PossessionLoader
from pbp.data_loader.segev_sports.enhanced_pbp.loader import SegevEnhancedPbpLoader
from pbp.resources.possessions.possession import Possession


class SegevPossessionLoader(PossessionLoader):
    client = MongoClient('localhost', 27017)
    db = client.PBP
    data_provider = 'segev_sports'
    resource = 'possessions'
    parent_object = 'Game'

    def __init__(self, game_id, source='web'):
        self.game_id = game_id
        self.source = source
        pbp_events = SegevEnhancedPbpLoader(game_id, source)
        self.events = pbp_events.items
        events_by_possession = self._split_events_by_possession()
        self.items = [Possession(possession_events) for possession_events in events_by_possession]
        self._add_extra_attrs_to_all_possessions()
        self._save_data_to_db()

    @property
    def data(self):
        return [item.export_data for item in self.items]

    def _save_data_to_db(self):
        self._save_data_to_db_by_game()
        for item in self.items:
            self._save_data_to_db_by_team(item)
            self._save_data_to_db_by_player(item)
            self._save_data_to_db_by_lineup(item)

    def _save_data_to_db_by_game(self):
        col = self.db.games
        col.update_one({'_id': int(self.game_id)}, {'$set': {'possessions': self.data}}, upsert=True)

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
            col.update_one({'_id': int(player_id)}, {'$addToSet': {'possessions.offense': item.export_data}}, upsert=True)
        for player_id in defense_lineup:
            col.update_one({'_id': int(player_id)}, {'$addToSet': {'possessions.defense': item.export_data}}, upsert=True)

    def _save_data_to_db_by_lineup(self, item):
        col = self.db.lineups
        offense_lineup = [int(p) for p in item.offense_lineup_id.split('-')]
        defense_lineup = [int(p) for p in item.defense_lineup_id.split('-')]
        col.update_one({'_id': item.offense_lineup_id}, {'$addToSet': {'possessions.offense': item.export_data},
                                                         '$set': {'player_ids': offense_lineup,
                                                                  'team_id': item.offense_team_id}},
                       upsert=True)
        col.update_one({'_id': item.defense_lineup_id}, {'$addToSet': {'possessions.defense': item.export_data},
                                                         '$set': {'player_ids': defense_lineup,
                                                                  'team_id': item.defense_team_id}},
                       upsert=True)

    def _save_data_to_file(self):
        with open('possessions.json', 'w') as outfile:
            json.dump(self.data, outfile, indent=4)
