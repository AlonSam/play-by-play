import pbp.resources.enhanced_pbp as e
from pbp.resources.enhanced_pbp import FreeThrow
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem


class SegevFreeThrow(FreeThrow, SegevEnhancedPbpItem):
    """
    class for Free Throw Events
    """
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def is_assisted(self):
        return self.is_made and hasattr(self, e.ASSIST_ID_STRING)
