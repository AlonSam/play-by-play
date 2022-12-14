from pydantic import Field

from pbp.models.custom_base_model import CustomBaseModel


class PlayerModel(CustomBaseModel):
    """
    TODO
    """
    id: str = Field(alias='_id')
    current_team_id: str
    name: str
    hebrew_name: str
    shirt_number: str

    @property
    def data(self):
        return self.dict(by_alias=True, exclude_none=True)