from pbp.resources.enhanced_pbp.deflection import Deflection
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem


class SegevDeflection(Deflection, SegevEnhancedPbpItem):
    """
    Class for deflection events
    """

    @property
    def export_data(self) -> dict:
        data = self.dict(by_alias=True, exclude_none=True, exclude={'previous_event', 'next_event'})
        data.update(self.base_data)
        return data