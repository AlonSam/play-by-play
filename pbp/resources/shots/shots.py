from pbp.resources.base import Base


class Shots(Base):
    """
    Class for shot items
    """

    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        return [item.data for item in self.items]