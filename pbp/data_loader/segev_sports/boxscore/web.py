import json
from typing import List, Dict

import pbp
from pbp.data_loader.segev_sports.web_loader import SegevWebLoader


class SegevBoxScoreWebLoader(SegevWebLoader):
    """
    Base class for loading segev_sports boxscores saved on database.
    This class should not be instantiated directly.
    """

    def load_data(self, game_id: str) -> List[Dict]:
        self.base_url = pbp.SEGEV_SCORES_BASE_URL + game_id
        self.source_data = self._load_request_data()
        self.source_data = self._get_items(game_id)
        return self.source_data

    def _get_items(self, game_id: str) -> List[Dict]:
        source_data = self.source_data['result']['boxscore']
        source_data = add_team_and_game_ids(source_data, game_id)
        teams = ['home', 'away']
        clean_data = []
        for side in teams:
            clean_data += [p for p in source_data[f'{side}Team']['players']]
            clean_data.append(source_data[f'{side}Team']['teamActions'])
        return [_fix_item(item) for item in clean_data]

    @property
    def data(self):
        return self.source_data


def _fix_item(item: Dict) -> Dict:
    item = fix_keys(item)
    item = {k: int(v) if isinstance(v, str) and v.isnumeric() else v for k, v in item.items()}
    item['treb'] = item['oreb'] + item['dreb']
    item['threepa'] = item['threepm'] + item.pop('fg_3mis')
    item['twopa'] = item['twopm'] + item.pop('fg_2mis')
    item['fta'] = item['ftm'] + item.pop('ft_mis')
    item['fgm'] = item['twopm'] + item['threepm']
    item['fga'] = item['twopa'] + item['threepa']
    item['twopct'] = cal_pct(item['twopm'], item['twopa'])
    item['threepct'] = cal_pct(item['threepm'], item['threepa'])
    item['fgpct'] = cal_pct(item['fgm'], item['fga'])
    item['ftpct'] = cal_pct(item['ftm'], item['fta'])
    new_item = dict()
    new_item['reb'] = dict(treb=item['treb'], dreb=item['dreb'], oreb=item['oreb'])
    new_item['fg'] = dict(made=item['fgm'], attempted=item['fga'], pct=item['fgpct'])
    new_item['two_pt'] = dict(made=item['twopm'], attempted=item['twopa'], pct=item['twopct'])
    new_item['three_pt'] = dict(made=item['threepm'], attempted=item['threepa'], pct=item['threepct'])
    new_item['ft'] = dict(made=item['ftm'], attempted=item['fta'], pct=item['ftpct'])
    new_item['fouls'] = dict(made=item['pf'], drawn=item['fd'])
    new_item['blocks'] = dict(made=item['blk'], blocked=item['blkd'])
    to_copy = ['player_id', 'team_id', 'game_id', 'shirt_num', 'starter', 'min', 'pm', 'stl', 'to', 'ast', 'fbpts',
               'scpts', 'pts', 'pir', 'dunk']
    new_item.update({k: v for k, v in item.items() if k in to_copy})
    return new_item


def fix_keys(item: Dict) -> Dict:
    with open("./data_loader/segev_sports/boxscore/rename.json") as json_data:
        rename_dict = json.load(json_data)
    item = {rename_dict[k] if k in rename_dict else k: v for k, v in item.items()}
    return item


def cal_pct(made: int, attempted: int) -> float:
    if attempted != 0:
        return round(made / attempted, 2)
    return 0


def add_team_and_game_ids(source_data: List[Dict], game_id: str) -> List[Dict]:
    teams = ['home', 'away']
    for side in teams:
        team_id = source_data['gameInfo'][f'{side}TeamId']
        for player in source_data[f'{side}Team']['players']:
            player['team_id'] = team_id
            player['game_id'] = game_id
        source_data[f'{side}Team']['teamActions']['player_id'] = 0
        source_data[f'{side}Team']['teamActions']['team_id'] = team_id
        source_data[f'{side}Team']['teamActions']['game_id'] = game_id
        source_data[f'{side}Team']['teamActions'].update(source_data['gameInfo'][f'{side}GameStats'])
    return source_data
