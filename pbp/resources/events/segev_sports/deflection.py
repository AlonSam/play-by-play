from pbp.resources.events.deflection import Deflection
from pbp.resources.events.segev_sports.event_item import SegevEventItem


class SegevDeflection(Deflection, SegevEventItem):
    """
    Class for deflection events
    """
    def __init__(self, *args):
        super().__init__(*args)