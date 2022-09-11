from pbp.resources.events.end_of_period import EndOfPeriod
from pbp.resources.events.segev_sports.event_item import SegevEventItem


class SegevEndOfPeriod(EndOfPeriod, SegevEventItem):
    """
    class for End of Period Events
    """
    def __init__(self, *args):
        super().__init__(*args)
