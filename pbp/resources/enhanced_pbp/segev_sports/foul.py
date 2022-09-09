from pbp.resources.enhanced_pbp import Foul
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem


class SegevFoul(Foul, SegevEnhancedPbpItem):
    """
    class for Foul Events
    """

    def __init__(self, *args):
        super().__init__(*args)