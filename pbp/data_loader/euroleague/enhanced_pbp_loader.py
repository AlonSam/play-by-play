from pbp.data_loader.enhanced_pbp_loader import EnhancedPbpLoader
from pbp.data_loader.euroleague.pbp_loader import ELPbpLoader


class ELEnhancedPbpLoader(ELPbpLoader, EnhancedPbpLoader):
    """
    Loads Euroleague enhanced pbp data for game.
    """
    def __init__(self, game_id, source, competition):
        super().__init__(game_id, source, competition)
        self.add_free_throw_count()
        self.combine_related_events()


game_id = '205'
competition = ['Euroleague', '2020', 'Regular Season']
pbp_loader = ELEnhancedPbpLoader(game_id, 'web', competition)