import abc


class AbsDataLoader(metaclass=abc.ABCMeta):
    """
    All data loaders will inherit from here
    """

    @abc.abstractmethod
    def data(self):
        pass