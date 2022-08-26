from pbp.resources.enhanced_pbp.rebound import Rebound
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem


class SegevRebound(Rebound, SegevEnhancedPbpItem):
    """
    class for Rebound Events
    """
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def export_data(self):
        data = {
            'action_type': 'Rebound',
            'is_offensive': self.is_offensive,
            'is_defensive': self.is_defensive,
            'missed_shot_event_id': self.missed_shot.event_id,
            'self_reb': self.self_reb,
        }
        base_data = self.base_data.copy()
        base_data.update(data)
        return base_data
