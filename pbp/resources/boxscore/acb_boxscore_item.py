rename_dict = {
    'id_team': 'team_id',
    'id_license': 'player_id',
    'pno': 'num',
    'points': 'pts',
    'time_played': 'tot_sec',
    '3pt_success': 'threepm',
    '3pt_tried': 'threepa',
    '3pt_percentage': 'threepct',
    '2pt_success': 'twopm',
    '2pt_tried': 'twopa',
    '2pt_percentage': 'twopct',
    '1pt_success': 'ftm',
    '1pt_tried': 'fta',
    '1pt_percentage': 'ftpct',
    'defensive_rebound': 'dreb',
    'offensive_rebound': 'oreb',
    'total_rebound': 'treb',
    'asis': 'ast',
    'steals': 'stl',
    'turnovers': 'tov',
    'blocks': 'blk',
    'received_blocks': 'blkd',
    'dunks': 'dunk',
    'personal_fouls': 'pf',
    'received_fouls': 'fd',
    'val': 'pir',
    'starting': 'starter',
    'playing': 'on_court',
    'differential': 'pm',

}


class ACBBoxScoreItem(object):
    """
    Class for boxscore items from ACB Spanish League

    :param dict item: dict with boxscore stats from response
    """
    def __init__(self, item, team_name=None):
        if 'tot_sec' not in item:
            if not item['id_license']:
                item['id_license'] = item['id_team']
            item = self.fix_item(item)
        for k, v in item.items():
            setattr(self, k, v)

    def fix_item(self, item):
        new_item = {rename_dict[k]: v for k, v in item.items() if k in rename_dict}
        if item['license']:
            new_item['player'] = item['license']['licenseStr15']
        else:
            new_item['player'] = 'team'
        if item['id_team'] == item['id_local_team']:
            new_item['team'] = item['local_team']['team_actual_name']
        else:
            new_item['team'] = item['visitor_team']['team_actual_name']
        new_item['threepct'] /= 100
        new_item['twopct'] /= 100
        new_item['ftpct'] /= 100
        new_item['fgm'] = new_item['threepm'] + new_item['twopm']
        new_item['fga'] = new_item['threepa'] + new_item['twopa']
        if new_item['fga'] > 0:
            new_item['fgpct'] = round(new_item['fgm'] / new_item['fga'], 2)
        else:
            new_item['fgpct'] = 0
        self.split_min(new_item)
        return new_item

    @staticmethod
    def split_min(item):
        item['min'] = item['tot_sec'] // 60
        item['sec'] = item['tot_sec'] - item['min']*60

    @property
    def data(self):
        return self.__dict__