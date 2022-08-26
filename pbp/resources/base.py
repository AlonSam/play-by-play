import abc


class Base(metaclass=abc.ABCMeta):
    """
    base class for all resources classes
    all resource classes should inherit from this
    """

    @abc.abstractmethod
    def data(self):
        pass