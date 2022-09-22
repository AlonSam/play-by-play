import numpy as np

KEY_ATTR_MAPPER = {
    'id': 'event_id',
    'parentActionId': 'parent_event_id',
    'type': 'action_type',
    'quarterTime': 'time',
    'quarter': 'period',
    'playerId': 'player_id',
    'teamId': 'team_id',
    'score': 'score'
}

ACTIONS_ATTR_MAPPER = {
    'foul-drawn': 'foul_on',
    'freeThrow': 'freethrow',
    'travelling': 'travel',
}

SHOT_ATTR_MAPPER = {
    'made': 'is_made',
    'fastBreak': 'is_fastbreak',
    'secondChancePoints': 'is_second_chance',
    'pointsFromTurnover': 'is_from_turnover',
    'coordX': 'x',
    'coordY': 'y',
    'points': 'shot_value'
}


class SegevPbpItem:
    """
    class for PBP events from segev_sports
    """
    def __init__(self, data):
        for key, value in KEY_ATTR_MAPPER.items():
            if data.get(key) is not None:
                setattr(self, value, str(data.get(key)))
        self._set_attributes(data)

    def _set_attributes(self, data):
        self.action_type = self.fix_actions(self.action_type)
        self.period = int(self.period)
        action_meta = data['parameters']
        if 'type' in action_meta.keys():
            self.sub_type = self.fix_actions(action_meta['type'])
        if self.action_type == 'quarter':
            self.action_type = self.sub_type
        elif self.action_type == 'substitution':
            if type(action_meta['playerOut']) == str:
                self.sub_type = 'out'
            elif type(action_meta['playerIn']) == str:
                self.sub_type = 'in'
            else:
                self.sub_type = None
        elif self.action_type == 'shot' or self.action_type == 'freethrow':
            for key, value in action_meta.items():
                if key in SHOT_ATTR_MAPPER.keys():
                    setattr(self, SHOT_ATTR_MAPPER.get(key), value)
            self.is_made = self.is_made == 'made'
            if self.action_type == 'shot':
                self.fix_coords()
                self.action_type = f'{self.shot_value}pt'
            else:
                self.sub_type = f'{action_meta["freeThrowNumber"]}of{action_meta["freeThrowsAwarded"]}'
        elif self.action_type == 'foul':
            self.foul_on = action_meta['fouledOn']
            self.free_throw = action_meta['freeThrows'] == "1"
            if action_meta['kind'] == 'offensive':
                self.sub_type = 'offensive'
            elif self.player_id == 0:
                if action_meta['isCoachFoul'] == 1:
                    self.sub_type = 'coach_technical'
                elif action_meta['isBenchFoul'] == 1:
                    self.sub_type = 'bench_technical'

    @staticmethod
    def fix_actions(act: str) -> str:
        if act in ACTIONS_ATTR_MAPPER.keys():
            return ACTIONS_ATTR_MAPPER[act]
        if '-' in act:
            return act.replace('-', '')
        return act

    def fix_coords(self):
        # self.x -= 70
        # if self.y < 500:
        #     if self.shot_value == 3:
        #         if 650 > self.x >= 80:
        #             self.x -= 60
        #         elif 1300 > self.x > 650:
        #             self.x += 80
        # self.x = round((self.x / 13.75), 2)
        # self.y = round(((self.y / 17.5) / 2), 2)
        # if self.x > 100:
        #     self.x -= 2
        # elif self.x < 0:
        #     self.x += 2
        # elif self.y < 20:
        #     if 68 > self.x > 55:
        #         self.x -= 6
        #     elif 45 > self.x > 32:
        #         self.x += 6
        # self.x = round(self.x*5, 2)
        # self.y = round((self.y*10), 2)
        x = self.x / 3
        y = (self.y / 3) * (14 / 15)
        # if self.shot_value == 3 and y < 250:
        #     x += (x - 250) * 0.2
        #     if y < 95:
        #         x -= (x - 250) * 0.05
        #     else:
        #         x, y = self.fix_distance(x, y, 0.9)
        # else:
        x += (x - 250) * 0.3
        y -= y * 0.1
        if self.shot_value == 3:
            if y < 100:
                x -= (x - 250) * 0.15
            elif 125 < x < 375:
                x, y = self.fix_distance(x, y, 0.9)
            else:
                x, y = self.fix_distance(x, y, 0.82)
            if self.is_inside_arc(x, y):
                if y < 100:
                    x, y = self.fix_distance(x, y, new_distance=225.0)
                else:
                    x, y = self.fix_distance(x, y, new_distance=235.0)
        else:
            x, y = self.fix_distance(x, y, 0.85)
        self.x = x
        self.y = y

    @staticmethod
    def is_inside_arc(x, y):
        rim = np.array((250.0, 52.5))
        point = np.array((x, y))
        distance = np.linalg.norm(point - rim)
        return distance < 225.0

    @staticmethod
    def fix_distance(x: float, y: float, ratio: float = None, new_distance: float = None):
        rim = np.array((250.0, 52.5))
        point = np.array((x, y))
        point_to_rim_vector = point - rim
        normalized_vector = point_to_rim_vector / np.linalg.norm(point_to_rim_vector)
        if new_distance is None:
            new_distance = np.linalg.norm(point_to_rim_vector) * ratio
        new_vector = normalized_vector * new_distance
        new_point = rim + new_vector
        return new_point



    @property
    def data(self):
        return self.__dict__


