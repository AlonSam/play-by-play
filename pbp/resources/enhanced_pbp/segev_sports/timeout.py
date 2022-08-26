from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem
from pbp.resources.enhanced_pbp.timeout import Timeout


class SegevTimeout(Timeout, SegevEnhancedPbpItem):
    """
    class for Timeout Events
    """
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def export_data(self):
        data = {
            'action_type': 'Timeout',
        }
        base_data = self.base_data.copy()
        base_data.update(data)
        return base_data
