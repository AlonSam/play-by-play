from pbp.resources.enhanced_pbp.end_of_period import EndOfPeriod
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem


class SegevEndOfPeriod(EndOfPeriod, SegevEnhancedPbpItem):
    """
    class for End of Period Events
    """
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def export_data(self):
        data = {
            'action_type': 'EndOfPeriod',
        }
        base_data = self.base_data.copy()
        base_data.update(data)
        return base_data