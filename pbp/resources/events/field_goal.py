import pbp


class FieldGoal(object):
    """
    Class for field goal events
    """
    event_type = ['2pt', '3pt']

    @property
    def is_corner_3(self):
        """
        returns True is shot was a corner 3, False otherwise
        """
        pass

    @property
    def is_heave(self) -> bool:
        """
        returns True if shot was taken at the last 2 seconds of a period and from an unreasonable distance
        """
        return self.shot_distance > pbp.HEAVE_DISTANCE_CUTOFF and self.seconds_remaining <= pbp.HEAVE_TIME_CUTOFF

    @property
    def rebound(self):
        """
        returns a :obj:`~pbp.resources.events.rebound.Rebound` object if shot was missed, None otherwise
        """
        if not self.is_made and self.next_event.action_type == 'rebound':
            return self.next_event

    @property
    def rebound_event_id(self) -> str:
        """
        returns the `event_id` attribute of the :obj:`~pbp.resources.events.rebound.Rebound` if exists, None otherwise.
        """
        return self.rebound.event_id if self.rebound else None

    @property
    def is_make_that_does_not_end_possession(self) -> bool:
        """
        returns True if shot was made but did not end the possession, False otherwise
        """
        return self.is_made and not self.is_possession_ending_event