from typing import List

from pbp.models.events.event_model import EventModel


class PossessionLoader(object):
    """
    Base class for all PossessionsLoaders
    All above should inherit from this class.
    This class should not be instantiated directly
    """

    def _split_events_by_possession(self) -> List[EventModel]:
        """
        splits events by possession
        :returns: list of lists with events for each possession
        """
        events = []
        possession_events = []
        for event in self.events:
            possession_events.append(event)
            if event.is_possession_ending_event:
                events.append(possession_events)
                possession_events = []
        return events