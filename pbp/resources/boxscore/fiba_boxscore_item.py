class FibaBoxScoreItem(object):
    """
    Class for boxscore items from FIBA Live Stats

    :param dict item: dict with boxscore stats from response
    """
    def __init__(self, item, team_name=None):
        if team_name:
            self.team_name = team_name
            if 'sBenchPoints' in item:
                item = self.fix_team_item(item)
            else:
                item = self.fix_player_item(item)
        for k, v in item.items():
            setattr(self, k, v)

    def fix_player_item(self, item):
        item = self.rename_items(item)
        self.split_min(item)
        item['player'] = f'{item["firstName"]} {item["familyName"]}'
        item = {k: v for k, v in item.items() if not self.del_keys(k)}
        return item

    def fix_team_item(self, item):
        item = self.rename_items(item)
        self.split_min(item)
        return item

    @staticmethod
    def split_min(item):
        if 'min' in item:
            item['sec'] = int(item['min'].split(':')[1])
            item['min'] = int(item['min'].split(':')[0])
            item['tot_sec'] = item['min'] * 60 + item['sec']

    @staticmethod
    def del_keys(k):
        return 'name' in k.lower() or 'eff' in k.lower() or 'photo' in k.lower() or k == 'comp'

    @property
    def data(self):
        return self.__dict__