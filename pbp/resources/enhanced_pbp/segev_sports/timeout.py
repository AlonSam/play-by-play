from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem
from pbp.resources.enhanced_pbp.timeout import Timeout


class SegevTimeout(Timeout, SegevEnhancedPbpItem):
    """
    class for Timeout Events
    """

    @property
    def export_data(self):
        data = self.dict(by_alias=True, exclude_none=True, exclude={'previous_event', 'next_event'})
        data.update(self.base_data)
        return data
