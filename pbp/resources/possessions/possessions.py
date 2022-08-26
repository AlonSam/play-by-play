"""
The ``Possessions`` class has some basic properties for aggregating possession stats
"""

from pbp.resources.base import Base

class Possessions(Base):
    """
    Class for possession items
    :param list items: list of
        :obj:`~pbpstats.resources.possessions.possession.Possession` items,
        typically from a possession data loader
    """

    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        """
        returns possessions dict
        """
        return self.__dict__