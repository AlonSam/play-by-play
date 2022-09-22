from fastapi import APIRouter

from api.database import (
    fetch_team,
    fetch_shots_for_instance
)
from models.api import TeamAPIModel

team_router = APIRouter()


@team_router.get("/get-team/{id}", summary="Retrieve a team's details by ID",
         tags=['General'], response_model=TeamAPIModel)
async def get_team(id: str):
    team = await fetch_team(id)
    if team:
        return team


@team_router.get("/get-shots/{id}", summary="Retrieve all shots taken by instance")
async def get_shots(id: str):
    shots = await fetch_shots_for_instance(id, 'team')
    if shots:
        return shots