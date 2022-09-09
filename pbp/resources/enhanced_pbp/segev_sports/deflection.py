from pbp.resources.enhanced_pbp.deflection import Deflection
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem


class SegevDeflection(Deflection, SegevEnhancedPbpItem):
    """
    Class for deflection events
    """
    def __init__(self, *args):
        super().__init__(*args)