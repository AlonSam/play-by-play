from pbp.resources.base import Base

class Teams(Base):
    """
    class for team items

    : param list items: list of either:
        :obj SegevTeamItem
        :obj FibaTeamItem
        :obj ELTeamItem
    """
    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        """
        returns list of dicts with game items
        """
        return [item.data for item in self.items]