from typing import Type

import pbp.resources.events.segev_sports as event_types
from pbp.resources.events.segev_sports.event_item import SegevEventItem


class SegevEventsFactory(object):
    """
    class for factory of event type classes. On initialization will load in all event classes
    in 'resources.events.segev_sports'
    """
    def __init__(self):
        self.event_classes = {}
        self._load_event_classes()

    def _load_event_classes(self) -> None:
        event_classes = dict([
            (name, cls) for name, cls in event_types.__dict__.items() if isinstance(cls, type)
        ])
        for _, event_cls in event_classes.items():
            if isinstance(event_cls.event_type, list):
                for event_type in event_cls.event_type:
                    self.event_classes[event_type] = event_cls
            else:
                self.event_classes[event_cls.event_type] = event_cls

    def get_event_class(self, event_type: str) -> Type[SegevEventItem]:
        """
        Gets the class for the event based on the event_type
        :param str event_type: event action type for the event
        :return: class for event type
        """
        return self.event_classes.get(event_type, SegevEventItem)
