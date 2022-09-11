from .event_model import EventModel


class TimeoutEventModel(EventModel):
    sub_type: str = None