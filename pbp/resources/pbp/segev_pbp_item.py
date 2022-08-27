from typing import Optional

from pydantic import BaseModel


class SegevPbpItem(BaseModel):
    """
    class for PBP events from segev_sports
    """
    event_id: int
    parent_event_id: int
    action_type: str
    sub_type: Optional[str]
    player_id: int
    team_id: int
    period: int
    time: str
    seconds_remaining: int
    score: Optional[str]
    is_made: Optional[bool]
    shot_value: Optional[int]
    x: Optional[float]
    y: Optional[float]
    is_fastbreak: Optional[bool]
    is_from_turnover: Optional[bool]
    is_second_chance: Optional[bool]
    free_throw: Optional[bool]
    foul_on: Optional[int]



