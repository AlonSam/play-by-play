import pbp
from pbp.data_loader.segev_sports.web_loader import SegevWebLoader


class SegevBoxScoreWebLoader(SegevWebLoader):
    """
    Base class for loading segev_sports boxscores saved on database.
    This class should not be instantiated directly.
    """

    def load_data(self, game_id):
        self.base_url = pbp.SEGEV_SCORES_BASE_URL + game_id
        return self._load_request_data()

    @property
    def data(self):
        return self.source_data