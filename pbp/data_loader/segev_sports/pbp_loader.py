import json
from os.path import exists
from typing import List, Dict

import pbp
from pbp.data_loader.segev_sports.loader import SegevLoader
from pbp.resources.pbp.segev_pbp_item import SegevPbpItem


class SegevPbpLoader(SegevLoader):
    """
    Loads segev_sports pbp data for game
    :param str game_id: segev_sports Game ID
    """

    def __init__(self, game_id: str):
        self.game_id = game_id
        self.source_data = self._load_data()
        self.check_overrides()
        self._make_pbp_items()

    def _load_data(self):
        self.base_url = pbp.SEGEV_ACTIONS_BASE_URL + self.game_id
        self.source_data = self._load_request_data()
        self.source_data = self.source_data['result']['actions']
        not_imp = ['clock', 'game']
        return [ev for ev in self.source_data if ev['type'] not in not_imp]

    def check_overrides(self):
        file_path = f'data_loader/segev_sports/overrides/{self.game_id}.json'
        if exists(file_path):
            with open(file_path, 'r') as readfile:
                data = json.load(readfile)
            self.source_data += data

    def _make_pbp_items(self):
        self.items = [SegevPbpItem(item) for item in self.source_data]
        self.items.sort(key=lambda x: x.event_id)

    @property
    def data(self) -> List[Dict]:
        return [item.data for item in self.items]

