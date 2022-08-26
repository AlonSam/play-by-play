import json
import os
from pathlib import Path

import requests

from file_loader import ELFileLoader
from pbp.resources.pbp.el_pbp_item import ELPbpItem
from web_loader import ELWebLoader


class ELPbpLoader(ELFileLoader, ELWebLoader):
    """
    Loads Euroleague pbp data for game
    :param str game_id: Euroleague Game ID
    :param str source: Where the data should be loaded from - file or web
    :param lst competition: List that contains the name of competition (EL or EC), season and phase in season.
    """
    base_directory = 'C:/Users/alons/PBP Database/'

    def __init__(self, game_id, source, competition):
        self.game_id = game_id
        self.source = source
        self.competition = competition
        if self.competition[0] == 'Euroleague':
            self.season = 'E' + self.competition[1]
        else:
            self.season = 'U' + self.competition[1]
        self.file_directory = self.base_directory + f'{competition[0]}/{competition[1]}/{game_id}'
        self._load_data()
        self.update_names()

    def _load_data(self):
        source_method = getattr(self, f'_from_{self.source}')
        source_method()

    def _from_file(self):
        """
        Loads pbp data from local file system
        """
        if not self.file_directory:
            raise ValueError('file_directory cannot be None when data source if file')
        self.file_path = f'{self.file_directory}/playbyplay.json'
        self._load_data_from_file()
        self._make_pbp_items()

    def _from_web(self):
        """
        Loads pbp data from web
        """
        self.base_url = f'http://live.euroleague.net/api/PlayByPlay?gamecode={self.game_id}&seasoncode={self.season}&disp='
        self._load_request_data()

    def combine_quarters(self):
        self.home_team = self.source_data['TeamA']
        self.source_data = self.source_data['FirstQuarter'] + self.source_data['SecondQuarter']\
                           + self.source_data['ThirdQuarter'] + self.source_data['ForthQuarter']\
                           + self.source_data['ExtraTime']
        self._load_shots()

    def _load_shots(self):
        shot_url = f'http://live.euroleague.net/api/Points?gamecode={self.game_id}&seasoncode={self.season}&disp='
        response = requests.get(shot_url)
        if response.status_code == 200:
            shot_data = response.json()
            self.add_shots(shot_data['Rows'])
        else:
            response.raise_for_status()

    def add_shots(self, shot_data):
        for item in self.source_data:
            if 'FG' in item['PLAYTYPE']:
                p = [ev for ev in shot_data if ev['NUM_ANOT'] == item['NUMBEROFPLAY']]
                ev = p[0]
                item['x'] = ev['COORD_X']
                item['y'] = ev['COORD_Y']
                item['fastbreak'] = (ev['FASTBREAK'] == '1')
                item['from_turnover'] = (ev['POINTS_OFF_TURNOVER'] == '1')
                item['second_chance'] = (ev['SECOND_CHANCE'] == '1')

    def add_margin(self):
        home_score = 0
        away_score = 0
        for item in self.source_data:
            if item['POINTS_A'] and item['POINTS_B']:
                home_score = item['POINTS_A']
                away_score = item['POINTS_B']
            elif item['POINTS_A']:
                item['POINTS_A'] = home_score
                item['POINTS_B'] = 0
            elif item['POINTS_B']:
                item['POINTS_A'] = 0
                item['POINTS_B'] = away_score
            else:
                item['POINTS_A'] = 0
                item['POINTS_B'] = 0
            if self.home_team == item['TEAM']:
                item['margin'] = item['POINTS_A'] - item['POINTS_B']
            else:
                item['margin'] = item['POINTS_B'] - item['POINTS_A']

    def _save_data_to_file(self):
        self.combine_quarters()
        self.add_margin()
        self._make_pbp_items()
        if self.file_directory:
            if not os.path.isdir(self.file_directory):
                os.makedirs(self.file_directory)
            file_path = f'{self.file_directory}/playbyplay.json'
            with open(file_path, 'w') as outfile:
                json.dump(self.data, outfile, indent=4)

    def _make_pbp_items(self):
        self.items = [ELPbpItem(item, self.home_team) for item in self.source_data]
        self.items.sort(key=lambda x: x.event_id)

    def update_names(self):
        names_path = 'names.json'
        data_file = Path(names_path)
        if not data_file.is_file():
            raise Exception(f'{names_path} does not exist')
        with open(names_path) as json_data:
            names_data = json.load(json_data)
        for item in self.items:
            if hasattr(item, 'player_id') and item.player_id not in names_data:
                names_data[item.player_id] = item.player
        with open(names_path, 'w') as outfile:
            json.dump(names_data, outfile, indent=4)

    @property
    def data(self):
        return [item.data for item in self.items]

game_id = '205'
competition = ['Euroleague', '2020', 'Regular Season']
pbp_loader = ELPbpLoader(game_id, 'web', competition)