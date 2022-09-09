from typing import List, Dict

import pbp
from pbp.data_loader.segev_sports.web_loader import SegevWebLoader


class SegevPbpWebLoader(SegevWebLoader):
    """
    Base class for loading segev_sports pbp events from web.
    """

    def load_data(self, game_id: str) -> List[Dict]:
        self.base_url = pbp.SEGEV_ACTIONS_BASE_URL + game_id
        self.source_data = self._load_request_data()
        self.source_data = self.source_data['result']['actions']
        not_imp = ['clock', 'game']
        return [self.fix_event(ev) for ev in self.source_data if ev['type'] not in not_imp]

    def fix_event(self, ev: Dict) -> Dict:
        action_desc = ev['parameters']
        action_type = self.fix_actions(ev['type'])
        new_item = {
            'event_id': ev['id'],
            'parent_event_id': ev['parentActionId'],
            'action_type': action_type,
            'time': ev['quarterTime'],
            'seconds_remaining': self.cal_sec_remaining(ev['quarterTime']),
            'period': ev['quarter'],
            'player_id': ev['playerId'],
            'team_id': ev['teamId'],
            'score': ev['score'] if 'score' in ev.keys() else None
            }
        if 'type' in action_desc.keys():
            new_item['sub_type'] = self.fix_actions(action_desc['type'])
        if action_type == 'quarter':
            new_item['action_type'] = new_item['sub_type']
        elif action_type == "substitution":
            if type(action_desc['playerOut']) == str:
                new_item['sub_type'] = "out"
            elif type(action_desc['playerIn']) == str:
                new_item['sub_type'] = "in"
            else:
                new_item['sub_type'] = None
        elif action_type == "shot" or action_type == "freethrow":
            new_item['is_made'] = action_desc['made'] == 'made'
            new_item['is_fastbreak'] = action_desc['fastBreak']
            new_item['is_second_chance'] = action_desc['secondChancePoints']
            new_item['is_from_turnover'] = action_desc['pointsFromTurnover']
            if action_type == "shot":
                new_item['x'] = action_desc['coordX']
                new_item['y'] = action_desc['coordY']
                new_item['shot_value'] = action_desc['points']
                new_item = self.fix_coords(new_item)
                new_item['action_type'] = f'{new_item["shot_value"]}pt'
            else:
                new_item['sub_type'] = f'{action_desc["freeThrowNumber"]}of{action_desc["freeThrowsAwarded"]}'
        elif action_type == "foul":
            new_item['foul_on'] = action_desc['fouledOn']
            new_item['free_throw'] = action_desc['freeThrows'] == "1"
            if action_desc['kind'] == 'offensive':
                new_item['sub_type'] = 'offensive'
        return new_item

    @staticmethod
    def cal_sec_remaining(clock: str) -> int:
        min, sec = clock.split(':')
        return int(min) * 60 + int(sec)

    @staticmethod
    def fix_actions(act: str) -> str:
        if act == "foul-drawn":
            return "foul_on"
        elif act == "freeThrow":
            return "freethrow"
        elif '-' in act:
            act = act.replace('-', '')
        elif act == "travelling":
            return "travel"
        return act

    @staticmethod
    def fix_coords(sh: Dict) -> Dict:
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

    @property
    def data(self):
        return self.source_data