from .event_model import EventModel


class FieldGoalEventModel(EventModel):
    is_made: bool
    x: float
    y: float
    shot_distance: float
    shot_type: str
    shot_value: int
    is_putback: bool
    is_assisted: bool
    is_blocked: bool
    is_heave: bool
    is_and_one: bool
    assist_player_id: str = None
    block_player_id: str = None
    rebound_event_id: str = None
