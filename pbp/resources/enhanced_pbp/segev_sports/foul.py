from typing import Optional

from pbp.resources.enhanced_pbp import Foul
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem


class SegevFoul(Foul, SegevEnhancedPbpItem):
    """
    class for Foul Events
    """
    foul_on_player_id: Optional[int]
    free_throw: Optional[bool]
    foul_on: Optional[int]

    @property
    def export_data(self):
        data = self.dict(by_alias=True, exclude_none=True, exclude={'previous_event', 'next_event'})
        data.update(self.base_data)
        return data