from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem
from pbp.resources.enhanced_pbp.timeout import Timeout


class SegevTimeout(Timeout, SegevEnhancedPbpItem):
    """
    class for Timeout Events
    """
    def __init__(self, *args):
        super().__init__(*args)
