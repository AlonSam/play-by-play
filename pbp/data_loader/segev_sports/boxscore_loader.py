from typing import List, Dict

import pbp
from pbp.data_loader.segev_sports.loader import SegevLoader
from pbp.models.boxscore_model import BoxScoreModel
from pbp.resources.boxscore.segev_boxscore_item import SegevBoxScoreItem


class SegevBoxScoreLoader(SegevLoader):
    """
        Loads segev_sports pbp data for game
        :param str game_id: segev_sports Game ID
        """
    def __init__(self, game_id: str):
        self.game_id = game_id
        self.source_data = self._load_data()
        self._make_boxscore_items()

    def _load_data(self):
        self.base_url = pbp.SEGEV_SCORES_BASE_URL + self.game_id
        source_data = self._load_request_data()
        clean_data = self._get_items(source_data)
        return clean_data

    def _get_items(self, source_data) -> List[Dict]:
        source_data = source_data['result']['boxscore']
        source_data = self._add_team_and_game_ids(source_data)
        sides = ['home', 'away']
        clean_data = []
        for side in sides:
            clean_data += [p for p in source_data[f'{side}Team']['players']]
            clean_data.append(source_data[f'{side}Team']['teamActions'])
        return clean_data

    def _add_team_and_game_ids(self, source_data: List[Dict]) -> List[Dict]:
        teams = ['home', 'away']
        for side in teams:
            team_id = source_data['gameInfo'][f'{side}TeamId']
            for player in source_data[f'{side}Team']['players']:
                player['team_id'] = team_id
                player['game_id'] = self.game_id
            source_data[f'{side}Team']['teamActions']['playerId'] = '0'
            source_data[f'{side}Team']['teamActions']['team_id'] = team_id
            source_data[f'{side}Team']['teamActions']['game_id'] = self.game_id
            source_data[f'{side}Team']['teamActions'].update(source_data['gameInfo'][f'{side}GameStats'])
        return source_data

    def _make_boxscore_items(self):
        self.items = [BoxScoreModel(**SegevBoxScoreItem(item).data) for item in self.source_data]

    @property
    def data(self) -> List[Dict]:
        return [item.data for item in self.items]