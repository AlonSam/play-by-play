from .event import Event

class SubstitutionEvent(Event):
    player_id: str = None
    sub_type: str = None
    sub_in_player_id: str
    sub_out_player_id: str = None
