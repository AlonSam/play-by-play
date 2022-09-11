from .event_model import EventModel

class SubstitutionEventModel(EventModel):
    player_id: str = None
    sub_type: str = None
    sub_in_player_id: str
    sub_out_player_id: str = None
