class FieldGoal(object):
    """
    Class for field goal events
    """
    event_type = ['2pt', '3pt']

    @property
    def rebound(self):
        """
        returns True is shot was rebounded, False otherwise
        """
        pass

    @property
    def is_corner_3(self):
        """
        returns True is shot was a corner 3, False otherwise
        """
        pass