from typing import Optional

from pydantic import validator

from pbp.resources.enhanced_pbp import FreeThrow
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem


class SegevFreeThrow(FreeThrow, SegevEnhancedPbpItem):
    """
    class for Free Throw Events
    """
    is_made: Optional[bool]
    assist_player_id: Optional[int]
    is_assisted: Optional[bool]
    @validator('is_assisted', always=True)
    def validate_is_assisted(cls, value, values):
        return values['is_made'] and values['assist_player_id'] is not None

    @property
    def export_data(self):
        data = self.dict(by_alias=True, exclude_none=True, exclude={'previous_event', 'next_event'})
        data.update(self.base_data)
        data.update({
            'isFirstFt': self.is_first_ft,
            'isLastFt': self.is_end_ft,
            'isTechnicalFt': self.is_technical_ft,
            'foulThatLedToFtEventId': self.foul_that_led_to_ft.event_id
        })
        return data
