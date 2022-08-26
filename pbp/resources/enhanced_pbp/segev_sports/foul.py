from pbp.resources.enhanced_pbp import Foul
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem


class SegevFoul(Foul, SegevEnhancedPbpItem):
    """
    class for Foul Events
    """
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def export_data(self):
        data = {
            'action_type': 'Foul',
            'type': self.sub_type,
            'foulon_player_id': self.foulon_player_id,
            'leads_to_ft': self.free_throw,
        }
        base_data = self.base_data.copy()
        base_data.update(data)
        return base_data