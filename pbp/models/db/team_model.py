from pydantic import Field

from pbp.models.custom_base_model import CustomBaseModel


class TeamModel(CustomBaseModel):
    """
    TODO
    """
    id: str = Field(alias='_id')
    name: str

    @property
    def data(self):
        return self.dict(by_alias=True, exclude_none=True)