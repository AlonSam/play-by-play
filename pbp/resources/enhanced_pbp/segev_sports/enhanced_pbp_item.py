from pbp.resources.enhanced_pbp import StartOfPeriod
from pbp.resources.enhanced_pbp.enhanced_pbp_item import EnhancedPbpItem


class SegevEnhancedPbpItem(EnhancedPbpItem):
    """
    Base class for enhanced pbp events from Segev Sports
    """
    def __init__(self, event):
        for key, value in event.dict().items():
            if value is not None:
                setattr(self, key, value)

    def __repr__(self):
        return f'{self.__class__.__name__}(event_id={self.event_id}, action_type={self.action_type}, game_id={self.game_id}, period={self.period}' \
               f', time={self.time}, team_id={self.team_id})'

    def __str__(self):
        return f'{self.action_type} ({self.sub_type})'

    @property
    def is_possession_ending_event(self):
        """
        returns True if event ends a possession, False otherwise
        """
        if self.next_event is None:
            return True
        if isinstance(self, StartOfPeriod):
            return False
        return self.offense_team_id != self.next_event.offense_team_id

    def get_all_related_events(self):
        """
        returns list of all directly related events to current event
        """
        events = [self]
        prev_id = self.previous_event_id
        if len(prev_id) == 0:
            # Check only forwards
            next_event = self.next_event
            while next_event and (next_event.event_id == prev_id or next_event.previous_event_id == prev_id):
                events.append(next_event)
                next_event = next_event.next_event
        # Check backwards
        prev_event = self.previous_event
        while prev_event and (prev_event.event_id == prev_id or prev_event.previous_event_id == prev_id):
            events.append(prev_event)
            prev_event = prev_event.previous_event
        return events