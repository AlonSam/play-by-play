from .event import Event


class ReboundEvent(Event):
    is_defensive: bool
    is_offensive: bool
    missed_shot_event_id: str
    missed_shot_type: str
    self_reb: bool
    is_team_rebound: bool