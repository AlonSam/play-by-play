from pbp.resources.enhanced_pbp import StartOfPeriod
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem

class InvalidNumberOfStartersException(Exception):
    """
    Class for exception when a team's 5 period starters can't be determined.
    You can add the correct period starters to
    overrides/missing_period_starters.json in your data directory to fix this.
    """

    pass


class SegevStartOfPeriod(StartOfPeriod, SegevEnhancedPbpItem):
    """
    class for Start Of Period Events
    """
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def players_on_court(self):
        """
        returns period starters
        """
        return self.period_starters
