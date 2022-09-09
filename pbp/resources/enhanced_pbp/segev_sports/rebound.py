import pbp.resources.enhanced_pbp as e
from pbp.resources.enhanced_pbp.rebound import Rebound
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem


class SegevRebound(Rebound, SegevEnhancedPbpItem):
    """
    class for Rebound Events
    """

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def is_offensive(self):
        return self.sub_type == e.OFFENSIVE_STRING

    @property
    def is_defensive(self):
        return self.sub_type == e.DEFENSIVE_STRING
