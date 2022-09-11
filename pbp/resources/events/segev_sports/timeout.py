from pbp.resources.events.segev_sports.event_item import SegevEventItem
from pbp.resources.events.timeout import Timeout


class SegevTimeout(Timeout, SegevEventItem):
    """
    class for Timeout Events
    """
    def __init__(self, *args):
        super().__init__(*args)
