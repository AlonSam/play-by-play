from pbp.resources.enhanced_pbp.deflection import Deflection
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_item import SegevEnhancedPbpItem


class SegevDeflection(Deflection, SegevEnhancedPbpItem):
    """
    Class for deflection events
    """

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def export_data(self):
        data = {
            'action_type': 'Deflection',
        }
        base_data = self.base_data.copy()
        base_data.update(data)
        return base_data