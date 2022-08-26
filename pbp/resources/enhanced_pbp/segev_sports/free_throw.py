from pbp.resources.enhanced_pbp import FreeThrow
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem


class SegevFreeThrow(FreeThrow, SegevEnhancedPbpItem):
    """
    class for Free Throw Events
    """
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def export_data(self):
        data = {
            'action_type': 'FreeThrow',
            'is_made': self.is_made,
            'type': self.sub_type,
            'is_first_ft': self.is_first_ft,
            'is_last_ft': self.is_end_ft,
            'is_technical_ft': self.is_technical_ft,
            'foul_that_led_to_ft_event_id': self.foul_that_led_to_ft.event_id,
            'is_assisted': self.is_assisted,
            'assist_player_id': self.assist_player_id if self.is_assisted else 0
        }
        base_data = self.base_data.copy()
        base_data.update(data)
        return base_data
