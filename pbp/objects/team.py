from typing import Optional, List

from pbp.objects.my_base_model import MyBaseModel


class Team(MyBaseModel):
    """
    TODO
    """
    id: int
    name: str
    competition: Optional[str]
    competitions: Optional[List[str]]
