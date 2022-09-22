from .api_base_model import APIBaseModel


class PlayerAPIModel(APIBaseModel):
    """
    TODO
    """
    id: str
    name: str
    hebrew_name: str
    team_name: str

    class Config:
        schema_extra = {
            "example": {
                "id": "2031",
                "name": "Scottie Wilbekin",
                "hebrewName": "סקוטי ווילבקין",
                "teamName": "Maccabi Tel Aviv"
            }
        }

    @property
    def data(self):
        return self.dict(by_alias=True, exclude_none=True)