rename_dict = {
    'order': 'event_id',
    'posX': 'x',
    'posY': 'y',
    'subType': 'sub_type',
    'crono': 'time',
    'score_local': 'home_score',
    'score_visitor': 'away_score',
    'id_team': 'team_id',
    'id_license': 'player_id',
    'lead': 'margin',
    'shirt_number': 'num'
}


class ACBPbpItem(object):
    """
    class for PBP events from ACB Spanish League
    """

    def __init__(self, item):
        if 'license' in item:
            item = self.fix_event(item)
        for k, v in item.items():
            setattr(self, k, v)

    def fix_event(self, item):
        new_item = {rename_dict[k]: v for k, v in item.items() if k in rename_dict.keys() and v}
        new_item['time'] = new_item['time'].split(':', 1)[1]
        new_item['period'] = item['period']
        new_item['seconds_remaining'] = self.cal_sec_remaining(new_item['time'])
        if item['team']:
            new_item['team'] = item['team']['team_actual_name']
        if item['license']:
            new_item['player'] = item['license']['licenseStr15']
        else:
            new_item['player'] = 'team'
        if item['type']['normalized_description']:
            action = item['type']['normalized_description']
        else:
            action = item['type']['description']
        new_item.update(self.fix_actions(action))
        if 'x' in new_item:
            new_item['x'], new_item['y'] = self.fix_coords(new_item['x'], new_item['y'])
        return new_item

    @staticmethod
    def cal_sec_remaining(clock):
        min, sec = clock.split(':')
        return int(min) * 60 + int(sec)

    @staticmethod
    def fix_coords(x, y):
        x = round(x / 280, 2) + 5
        if y > 0:
            y = (y / 155) + 50
        elif y < 0:
            y = 50 - (y / -155)
        else:
            y += 50
        y = round(y, 2)
        return x, y

    @staticmethod
    def fix_actions(act):
        act = act.lower()
        action_type = str()
        sub_type = str()
        made = None
        if 'substitution' in act:
            action_type, sub_type = act.split(' - ')
        elif ('start' in act and 'ing' not in act) or 'end' in act:
            action_type, _, _, sub_type = act.split(' ')
            if sub_type == 'quarter':
                sub_type = 'period'
        elif 'jump' in act:
            action_type = 'jumpball'
            sub_type = act.split(' ')[0]
        elif 'foul' in act and 'assist' not in act:
            if 'received' in act:
                action_type = 'foulon'
            else:
                action_type = 'foul'
                if 'no ft' in act:
                    sub_type = 'personal'
                elif 'technical' in act:
                    sub_type = 'technical'
                elif '2ft' in act or '3ft' in act:
                    sub_type = 'shooting'
                elif '1ft' in act:
                    sub_type = 'and_one'
                elif 'unsportsmanlike' in act:
                    sub_type = 'unsportsmanlike'
                elif 'offensive' in act:
                    sub_type = 'offensive'
                else:
                    print(act)
        elif 'unsportsmanlike' in act:
            action_type = 'foul'
            sub_type = 'unsportsmanlike'
        elif ('made' in act or 'missed' in act or act == 'dunk') and 'fast' not in act:
            made = ('made' in act or act == 'dunk')
            if '2' in act or 'dunk' in act:
                action_type = '2pt'
                if 'dunk' in act:
                    sub_type = 'dunk'
            elif '3' in act:
                action_type = '3pt'
            elif 'free throw' in act:
                action_type = 'freethrow'
            else:
                print(act)
        elif 'rebound' in act:
            action_type = 'rebound'
            sub_type = act.split(' ')[0]
        elif 'assist' in act:
            action_type = 'assist'
        elif 'timeout' in act:
            action_type = 'timeout'
        elif act == 'block received':
            action_type = 'blocked'
        else:
            action_type = act
        d = {'action_type': action_type, 'sub_type': sub_type}
        if made is not None:
            d['made'] = made
        return d

    @property
    def data(self):
        return self.__dict__