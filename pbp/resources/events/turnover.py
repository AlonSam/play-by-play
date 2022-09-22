from abc import abstractmethod


class Turnover(object):
    """
    Class for Turnover events
    """
    event_type = 'turnover'

    @property
    @abstractmethod
    def is_steal(self):
        pass

    @property
    @abstractmethod
    def is_bad_pass(self):
        pass

    @property
    @abstractmethod
    def is_ball_handling(self):
        pass

    @property
    @abstractmethod
    def is_travel(self):
        pass

    @property
    @abstractmethod
    def is_shot_clock_violation(self):
        pass

    @property
    @abstractmethod
    def is_3_second_violation(self):
        pass

    @property
    @abstractmethod
    def is_5_second_violation(self):
        pass

    @property
    @abstractmethod
    def is_8_second_violation(self):
        pass

    @property
    @abstractmethod
    def is_out_of_bounds(self):
        pass

    @property
    @abstractmethod
    def is_offensive_foul(self):
        pass

    @property
    @abstractmethod
    def is_backcourt_violation(self):
        pass

    @property
    @abstractmethod
    def is_double_dribble(self):
        pass
