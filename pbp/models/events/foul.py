from pydantic import validator

from .event import Event


class FoulEvent(Event):
    free_throw: bool
    foul_on_player_id: str = None
    is_offensive_foul: bool
    is_and_one_foul: bool
    is_personal_foul: bool
    is_shooting_foul: bool
    is_technical: bool
    is_unsportsmanlike_foul: bool

    @validator('foul_on_player_id')
    def validate_foul_on_player_id(cls, value, values):
        if value:
            return value
        if getattr(values, 'is_technical'):
            return value
        raise ValueError('Foul Event does not have `foul_on_player_id`')