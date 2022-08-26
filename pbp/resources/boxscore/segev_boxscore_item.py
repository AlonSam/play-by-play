import json


class SegevBoxScoreItem(object):
    """
    Class for boxscore items from Segev Sports

    :param dict item: dict with boxscore stats from response
    """
    def __init__(self, item, game_id, team_id=None):
        self.game_id = int(game_id)
        if team_id:
            self.team_id = team_id
            item = self.fix_item(item)
        for k, v in item.items():
            setattr(self, k, v)

    def fix_item(self, item):
        item = self.rename_items(item)
        item = {k: int(v) if isinstance(v, str) and v.isnumeric() else v for k, v in item.items()}
        item['treb'] = item['oreb'] + item['dreb']
        item['threepa'] = item['threepm'] + item.pop('fg_3mis')
        item['twopa'] = item['twopm'] + item.pop('fg_2mis')
        item['fta'] = item['ftm'] + item.pop('ft_mis')
        item['fgm'] = item['twopm'] + item['threepm']
        item['fga'] = item['twopa'] + item['threepa']
        item['twopct'] = self.cal_pct(item['twopm'], item['twopa'])
        item['threepct'] = self.cal_pct(item['threepm'], item['threepa'])
        item['fgpct'] = self.cal_pct(item['fgm'], item['fga'])
        item['ftpct'] = self.cal_pct(item['ftm'], item['fta'])

        new_item = dict()
        new_item['reb'] = dict(treb=item['treb'], dreb=item['dreb'], oreb=item['oreb'])
        new_item['fg'] = dict(made=item['fgm'], attempted=item['fga'], pct=item['fgpct'])
        new_item['2pt'] = dict(made=item['twopm'], attempted=item['twopa'], pct=item['twopct'])
        new_item['3pt'] = dict(made=item['threepm'], attempted=item['threepa'], pct=item['threepct'])
        new_item['ft'] = dict(made=item['ftm'], attempted=item['fta'], pct=item['ftpct'])
        new_item['fouls'] = dict(made=item['pf'], drawn=item['fd'])
        new_item['blocks'] = dict(made=item['blk'], blocked=item['blkd'])
        new_item['team_id'] = int(self.team_id)
        to_copy = ['player_id', 'shirt_num', 'starter', 'min', 'pm', 'stl', 'to', 'ast', 'fbpts', 'scpts', 'pts', 'pir',
                   'dunk']
        new_item.update({k: v for k, v in item.items() if k in to_copy})
        return new_item

    @staticmethod
    def cal_pct(made, attempted):
        if attempted != 0:
            return round(made/attempted, 2)
        return 0

    def rename_items(self, item):
        with open('C:/Users/alons/PycharmProjects/PlaybyPlay/pbp/resources/boxscore/rename.json') as json_data:
            rename_dict = json.load(json_data)
        item = {rename_dict[k] if k in rename_dict else k: v for k, v in item.items()}
        return item

    @property
    def data(self):
        return self.__dict__
