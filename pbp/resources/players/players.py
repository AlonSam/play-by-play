from pbp.resources.base import Base

class Players(Base):
    """
    class for player items

    : param list items: list of either:
        :obj SegevPlayerItem
        :obj FibaPlayerItem
        :obj ELPlayerItem
    """
    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        """
        returns list of dicts with game items
        """
        return [item.data for item in self.items]