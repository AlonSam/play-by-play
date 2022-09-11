import pbp.resources.events as e
from pbp.resources.events import Foul
from pbp.resources.events.segev_sports.event_item import SegevEventItem


class SegevFoul(Foul, SegevEventItem):
    """
    class for Foul Events
    """

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def is_personal_foul(self):
        return self.sub_type == e.PERSONAL_STRING

    @property
    def is_shooting_foul(self):
        if self.sub_type == e.SHOOTING_STRING or self.sub_type == e.AND_ONE_STRING:
            return True
        if self.sub_type == e.PERSONAL_STRING and self.free_throw and self.fouls_to_give[self.team_id] > 0:
            return True
        return False

    @property
    def is_offensive_foul(self):
        return self.sub_type == e.OFFENSIVE_STRING

    @property
    def is_and_one_foul(self):
        return self.sub_type == e.AND_ONE_STRING

    @property
    def is_technical(self):
        return e.TECHNICAL_STRING in self.sub_type

    @property
    def is_unsportsmanlike_foul(self):
        return self.sub_type == e.UNSPORTSMANLIKE_STRING

    @property
    def counts_towards_penalty(self):
        return self.counts_as_personal_foul

    @property
    def counts_as_personal_foul(self):
        """
        returns True if foul was made by a player, False otherwise (in case of coach/bench technical)
        """
        if self.sub_type == 'coach_technical' or self.sub_type == 'bench_technical':
            return False
        return True
