from pbp.resources.base import Base


class Pbp(Base):
    """
    Class for PBP items
    """

    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        """
        returns list of dicts for each event
        """
        return [item.data for item in self.items]