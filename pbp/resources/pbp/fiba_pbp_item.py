rename_dict = {
    'actionNumber': 'event_id',
    'previousAction': 'previous_event_id',
    'actionType': 'action_type',
    'subType': 'sub_type',
    'gt': 'time',
    's1': 'home_score',
    's2': 'away_score',
    'tno': 'team_id',
    'pno': 'player_id',
    'lead': 'margin',
    'shirtNumber': 'num'
}


class FibaPbpItem(object):
    """
    class for PBP events from FIBA Live Stats
    """

    def __init__(self, event):
        if 'qualifier' in event:
            event = self.fix_event(event)
        for k, v in event.items():
            setattr(self, k, v)

    def fix_event(self, event):
        item = {rename_dict[k] if k in rename_dict else k: v for k, v in event.items()}
        if self.is_overtime(item):
            item['period'] = 5
        if item['scoring'] == 1:
            item['made'] = (item['success'] == 1)
        if item['player_id'] != 0:
            item['player'] = f'{item["firstName"]} {item["familyName"]}'
        else:
            item['player'] = 'team'
        if item['team_id'] == 2:
            item['margin'] *= -1
        if len(item['qualifier']) > 0:
            item['in_paint'] = ('pointsinthepaint' in item['qualifier'])
            item['from_turnover'] = ('fromturnover' in item['qualifier'])
            item['second_chance'] = ('2ndchance' in item['qualifier'])
            item['fastbreak'] = ('fastbreak' in item['qualifier'])
            if item['action_type'] == 'foul' and item['sub_type'] == 'personal':
                if 'shooting' in item['qualifier']:
                    if '2freethrow' in item['qualifier']:
                        item['sub_type'] = 'shooting'
                    else:
                        item['sub_type'] = 'and_one'
                elif '2freethrow' in item['qualifier']:
                    item['sub_type'] = 'bonus'
        item['seconds_remaining'] = self.cal_sec_remaining(item['time'])
        if item['sub_type'] == 'start' or item['sub_type'] == 'end':
            item['action_type'], item['sub_type'] = item['sub_type'], item['action_type']
        item = {k: v for k, v in item.items() if not(self.del_keys(k))}
        return item

    @staticmethod
    def cal_sec_remaining(clock):
        min, sec = clock.split(':')
        return int(min) * 60 + int(sec)

    @staticmethod
    def is_overtime(ev):
        return 'periodType' in ev and ev['periodType'] == 'OVERTIME'

    @staticmethod
    def del_keys(k):
        unnec_keys = ['qualifier', 'scoring', 'periodType', 'success', 'clock']
        return k in unnec_keys or 'name' in k.lower()

    @property
    def data(self):
        return self.__dict__