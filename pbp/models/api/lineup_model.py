from models.api.api_base_model import APIBaseModel


class LineupAPIModel(APIBaseModel):
    id: str
    players: str
    team_name: str
    team_id: str


    @property
    def data(self):
        return self.dict(by_alias=True, exclude_none=True)