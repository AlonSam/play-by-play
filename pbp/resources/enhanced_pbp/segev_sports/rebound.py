from typing import Optional

from pydantic import validator

from pbp.resources.enhanced_pbp.rebound import Rebound
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem


class SegevRebound(Rebound, SegevEnhancedPbpItem):
    """
    class for Rebound Events
    """
    is_offensive: Optional[bool]
    is_defensive: Optional[bool]

    @validator('is_offensive', always=True)
    def validate_is_offensive(cls, value, values):
        return values['sub_type'] == 'offensive'

    @validator('is_defensive', always=True)
    def validate_is_defensive(cls, value, values):
        return values['sub_type'] == 'defensive'

    @property
    def export_data(self):
        data = self.dict(by_alias=True, exclude_none=True, exclude={'previous_event', 'next_event'})
        data.update(self.base_data)
        data.update({
            'missedShotEventId': self.missed_shot.event_id,
            'selfRebound': self.self_reb
        })
        return data
