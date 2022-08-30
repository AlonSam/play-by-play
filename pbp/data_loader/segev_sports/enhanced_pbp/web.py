from pbp.data_loader.segev_sports.pbp.loader import SegevPbpLoader
from pbp.data_loader.segev_sports.web_loader import SegevWebLoader


class SegevEnhancedPbpWebLoader(SegevWebLoader):
    """
    TODO
    """
    def load_data(self, game_id):
        return SegevPbpLoader.from_web(game_id).items
