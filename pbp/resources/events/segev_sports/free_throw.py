import pbp.resources.events as e
from pbp.resources.events import FreeThrow
from pbp.resources.events.segev_sports.event_item import SegevEventItem


class SegevFreeThrow(FreeThrow, SegevEventItem):
    """
    class for Free Throw Events
    """
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def is_assisted(self):
        return self.is_made and hasattr(self, e.ASSIST_ID_STRING)
