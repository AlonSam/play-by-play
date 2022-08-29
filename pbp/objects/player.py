from typing import Optional

from pbp.objects.my_base_model import MyBaseModel


class Player(MyBaseModel):
    """
    TODO
    """
    id: int
    team_id: int
    name: str
    hebrew_name: Optional[str]
    shirt_number: Optional[int]
