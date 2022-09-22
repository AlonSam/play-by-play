import pbp.resources.events as e
from pbp.resources.events.rebound import Rebound
from pbp.resources.events.segev_sports.event_item import SegevEventItem


class SegevRebound(Rebound, SegevEventItem):
    """
    class for Rebound Events
    """

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def is_offensive(self):
        return self.sub_type == e.OFFENSIVE_STRING

    @property
    def is_defensive(self):
        return self.sub_type == e.DEFENSIVE_STRING


