from __future__ import annotations

from .api_base_model import APIBaseModel


class TeamAPIModel(APIBaseModel):
    """
    TODO
    """
    id: str
    name: str

    class Config:
        schema_extra = {
            "example": {
                "id": "2",
                "name": "Maccabi Tel Aviv"
            }
        }

    @property
    def data(self):
        return self.dict(by_alias=True, exclude_none=True)