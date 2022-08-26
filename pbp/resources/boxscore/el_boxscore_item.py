class ELBoxScoreItem(object):
    """
    Class for boxscore items from Euroleague

    :param dict item: dict with boxscore stats from response
    """
    def __init__(self, item, team_name=None):
        if 'tot_sec' not in item:
            item = self.fix_item(item)
        for k, v in item.items():
            setattr(self, k, v)

    def fix_item(self, item):
        self.split_min(item)
        item['player'] = self.fix_player_name(item['player'])
        return item

    @staticmethod
    def fix_player_name(pl):
        if ',' in pl:
            last, first = pl.split(',')
            if len(last.split(' ')) > 1:
                last_names = last.split(' ')
                last = ''
                for nm in last_names:
                    last += nm.capitalize()
                name = f'{first.strip().capitalize()} {last}'
            else:
                name = f'{first.strip().capitalize()} {last.capitalize()}'
            return name
        return pl

    @staticmethod
    def split_min(item):
        if item['min'] != 0:
            item['sec'] = int(item['min'].split(':')[1])
            item['min'] = int(item['min'].split(':')[0])
            item['tot_sec'] = item['min'] * 60 + item['sec']

    @property
    def data(self):
        return self.__dict__