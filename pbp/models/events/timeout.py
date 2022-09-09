from .event import Event


class TimeoutEvent(Event):
    sub_type: str = None