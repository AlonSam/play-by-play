from .event import Event


class FreeThrowEvent(Event):
    is_made: bool
    is_first_ft: bool
    is_end_ft: bool
    is_ft_1_of_1: bool
    is_ft_1_of_2: bool
    is_ft_1_of_3: bool
    is_ft_2_of_2: bool
    is_ft_2_of_3: bool
    is_ft_3_of_3: bool
    is_technical_ft: bool
    is_assisted: bool
    assist_player_id: str = None
    foul_that_led_to_ft_event_id: str
