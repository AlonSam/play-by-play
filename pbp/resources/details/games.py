from pbp.resources.base import Base

class Details(Base):
    """
    class for game items

    : param list items: list of either:
        :obj SegevDetailsItem
        :obj FibaDetailsItem
        :obj ELDetailsItem
    """
    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        """
        returns list of dicts with game items
        """
        return [item.data for item in self.items]

    @property
    def final_games(self):
        """
        return list of dicts with final game items
        """
        return [item.data for item in self.items if item.is_final]