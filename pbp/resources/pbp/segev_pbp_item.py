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
        self.seconds_remaining = self.get_sec_remaining()
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

    def get_sec_remaining(self) -> int:
        min, sec = self.time.split(':')
        return int(min) * 60 + int(sec)

    @staticmethod
    def fix_actions(act: str) -> str:
        if act in ACTIONS_ATTR_MAPPER.keys():
            return ACTIONS_ATTR_MAPPER[act]
        if '-' in act:
            return act.replace('-', '')
        return act

    def fix_coords(self):
        self.x -= 70
        if self.y < 500:
            if self.shot_value == 3:
                if 650 > self.x >= 80:
                    self.x -= 60
                elif 1300 > self.x > 650:
                    self.x += 80
        self.x = round((self.x / 13.75), 2)
        self.y = round(((self.y / 17.5) / 2), 2)
        if self.x > 100:
            self.x -= 2
        elif self.x < 0:
            self.x += 2
        elif self.y < 20:
            if 68 > self.x > 55:
                self.x -= 6
            elif 45 > self.x > 32:
                self.x += 6
        temp = self.x
        self.x = round(self.y, 2)
        self.y = 100 - round(temp, 2)

    @property
    def data(self):
        return self.__dict__


