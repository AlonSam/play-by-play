from typing import Dict

import pbp
from pbp.data_loader.segev_sports.loader import SegevLoader
from pbp.models.details_model import DetailsModel
from pbp.models.player_model import PlayerModel
from pbp.resources.details.segev_details_item import SegevDetailsItem


class SegevDetailsLoader(SegevLoader):
    """
        Loads segev_sports pbp data for game
        :param str game_id: segev_sports Game ID
        :param str source: Where the data should be loaded from - db or web
        """

    def __init__(self, basket_id: str):
        self.basket_id = basket_id
        self._load_data()
        self._make_game_item()

    def _load_data(self):
        self.basket_data = self._load_basket_data(self.basket_id)
        self.game_id = str(self.basket_data['ExternalID'])
        self.base_url = pbp.SEGEV_ACTIONS_BASE_URL + self.game_id
        self.source_data = self._load_request_data()
        self.source_data = self.source_data['result']['gameInfo']
        self.players = self.get_players()

    def _load_basket_data(self, basket_id):
        self.base_url = pbp.BASKET_GAME_DATA_BASE_URL + basket_id
        base_data = self._load_request_data()
        return base_data[0]['games'][0]

    def _make_game_item(self):
        self.item = DetailsModel(**SegevDetailsItem(self.basket_data, self.source_data).data)

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
                players.append(PlayerModel(**data))
        return players

    @staticmethod
    def capitalize_name(first_name, last_name):
        name = first_name.capitalize()
        for n in last_name.split(' '):
            name += ' ' + n.capitalize()
        return name

    @property
    def data(self) -> Dict:
        return self.item.data
