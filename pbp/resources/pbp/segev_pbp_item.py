class SegevPbpItem(object):
    """
    class for PBP events from segev_sports
    """

    def __init__(self, item):
        if 'parameters' in item:
            item = self.fix_event(item)
        for k, v in item.items():
            setattr(self, k, v)

    @property
    def data(self):
        return self.__dict__

    def fix_event(self, ev):
        new_item = dict()
        action_desc = ev['parameters']
        new_item['event_id'] = ev['id']
        new_item['previous_event_id'] = ev['parentActionId']
        new_item['action_type'] = self.fix_actions(ev['type'])
        new_item['time'] = ev['quarterTime']
        new_item['seconds_remaining'] = self.cal_sec_remaining(new_item['time'])
        new_item['period'] = ev['quarter']
        new_item['player_id'] = ev['playerId']
        new_item['team_id'] = ev['teamId']
        if 'score' in ev.keys():
            new_item['score'] = ev['score']
        if 'type' in action_desc.keys():
            new_item['sub_type'] = self.fix_actions(action_desc['type'])
        if new_item['action_type'] == 'quarter':
            new_item['action_type'] = new_item['sub_type']
        if ev['type'] == "substitution":
            if type(action_desc['playerOut']) == str:
                new_item['sub_type'] = "out"
            elif type(action_desc['playerIn']) == str:
                new_item['sub_type'] = "in"
            else:
                new_item['sub_type'] = None
        elif ev['type'] == "shot" or ev['type'] == "freeThrow":
            new_item['is_made'] = action_desc['made'] == 'made'
            new_item['is_fastbreak'] = action_desc['fastBreak']
            new_item['is_second_chance'] = action_desc['secondChancePoints']
            new_item['is_from_turnover'] = action_desc['pointsFromTurnover']
            if ev['type'] == "shot":
                new_item['x'] = action_desc['coordX']
                new_item['y'] = action_desc['coordY']
                new_item['shot_value'] = action_desc['points']
                new_item = self.fix_coords(new_item)
                new_item['action_type'] = f'{new_item["shot_value"]}pt'
            else:
                new_item['sub_type'] = f'{action_desc["freeThrowNumber"]}of{action_desc["freeThrowsAwarded"]}'
        elif ev['type'] == "foul":
            new_item['foulon'] = action_desc['fouledOn']
            new_item['free_throw'] = action_desc['freeThrows'] == "1"
            if action_desc['kind'] == 'offensive':
                new_item['sub_type'] = 'offensive'

        return new_item

    @staticmethod
    def cal_sec_remaining(clock):
        min, sec = clock.split(':')
        return int(min) * 60 + int(sec)

    @staticmethod
    def fix_actions(act):
        if act == "foul-drawn":
            return "foulon"
        elif act == "freeThrow":
            return "freethrow"
        elif '-' in act:
            act = act.replace('-', '')
        elif act == "travelling":
            return "travel"
        return act


    @staticmethod
    def fix_coords(sh):
        sh['x'] -= 70
        if sh['y'] < 500:
            if sh['shot_value'] == 3:
                if 650 > sh['x'] >= 80:
                    sh['x'] -= 60
                elif 1300 > sh['x'] > 650:
                    sh['x'] += 80
        sh['x'] = round((sh['x'] / 13.75), 2)
        sh['y'] = round(((sh['y'] / 17.5) / 2), 2)
        if sh['x'] > 100:
            sh['x'] -= 2
        elif sh['x'] < 0:
            sh['x'] += 2
        elif sh['y'] < 20:
            if 68 > sh['x'] > 55:
                sh['x'] -= 6
            elif 45 > sh['x'] > 32:
                sh['x'] += 6
        temp = sh['x']
        sh['x'] = round(sh['y'], 2)
        sh['y'] = 100 - round(temp, 2)
        return sh