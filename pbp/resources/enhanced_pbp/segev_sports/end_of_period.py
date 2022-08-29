from pbp.resources.enhanced_pbp.end_of_period import EndOfPeriod
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem


class SegevEndOfPeriod(EndOfPeriod, SegevEnhancedPbpItem):
    """
    class for End of Period Events
    """

    @property
    def export_data(self) -> dict:
        data = self.dict(by_alias=True, exclude_none=True, exclude={'previous_event', 'next_event'})
        data.update(self.base_data)
        return data