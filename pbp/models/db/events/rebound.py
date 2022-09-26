from .event_model import EventModel


class ReboundEventModel(EventModel):
    is_defensive: bool
    is_offensive: bool
    missed_shot_event_id: str
    missed_shot_zone: str
    self_reb: bool
    is_team_rebound: bool