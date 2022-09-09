from datetime import datetime

import pbp
from pbp.data_loader.segev_sports.details import *
from pbp.data_loader.segev_sports.web_loader import SegevWebLoader
from pbp.objects.player import Player


class SegevDetailsWebLoader(SegevWebLoader):
    """
    Base class for loading segev_sports details saved on database.
    This class should not be instantiated directly.
    """

    def load_data(self, basket_id):
        basket_data = self.load_basket_data(basket_id)
        game_id = str(basket_data['game_id'])
        self.base_url = pbp.SEGEV_ACTIONS_BASE_URL + game_id
        self.source_data = self._load_request_data()
        self.source_data = self.source_data['result']['gameInfo']
        players = self.get_players()
        self.source_data = self.fix_details(basket_data)
        return self.source_data, players

    def load_basket_data(self, basket_id):
        self.base_url = pbp.BASKET_GAME_DATA_BASE_URL + basket_id
        base_data = self._load_request_data()
        base_data = base_data[0]['games'][0]
        basket_data = {
            'basket_id': base_data['id'],
            'game_id': base_data['ExternalID'],
            'season': str(base_data['game_year']),
            'phase': PHASES[str(base_data['game_type'])],
            'round': base_data['GN'],
            'home_score': base_data['score_team1'],
            'away_score': base_data['score_team2'],
            'attendance': base_data['total_viewers'],
            'referees': [ref.strip() for ref in base_data['ref_eng'].split(',')],
            'observer': base_data['observer_eng'].strip()
        }
        return basket_data

    def get_players(self):
        names = ['home', 'away']
        players = []
        for name in names:
            raw_players = self.source_data[f'{name}Team']['players']
            team_id = self.source_data[f'{name}Team']['id']
            for player in raw_players:
                data = dict(id=player['id'],
                            team_id=team_id,
                            name=self.capitalize_name(player['firstName'], player['lastName']),
                            hebrew_name=player['firstNameLocal'] + ' ' + player['lastNameLocal'],
                            shirt_number=player['jerseyNumber'])
                players.append(Player.parse_obj(data))
        return players

    @staticmethod
    def capitalize_name(first_name, last_name):
        name = first_name.capitalize()
        for n in last_name.split(' '):
            name += ' ' + n.capitalize()
        return name

    def fix_details(self, basket_data):
        new_item = basket_data
        new_item.update({
            'final': self.is_finished(self.source_data),
            'time': datetime.strptime(self.source_data['time'], '%Y-%m-%dT%H:%M:%S'),
            'home_team': self.fix_name(self.source_data['homeTeam']['name']),
            'home_id': int(self.source_data['homeTeam']['id']),
            'away_team': self.fix_name(self.source_data['awayTeam']['name']),
            'away_id': int(self.source_data['awayTeam']['id']),
            'competition': self.source_data['competition']['name']
        })
        return new_item

    @staticmethod
    def is_finished(item):
        return item['gameFinished'] or item['currentQuarter'] == 4 and item['currentQuarterTime']['m'] == 0\
        and item['currentQuarterTime']['s'] == 0

    @staticmethod
    def fix_name(tm):
        if tm in TEAM_NAMES.keys():
            return TEAM_NAMES[tm]
        else:
            names = tm.split(' ')
            team = ''
            for name in names:
                team += name.capitalize() + ' '
            return team.strip()

    @property
    def data(self):
        return self.source_data
