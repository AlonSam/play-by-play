from fastapi import APIRouter

from api.database import (
    fetch_player
)
from models.api import PlayerAPIModel

player_router = APIRouter()


@player_router.get("/get-player/{id}", summary="Retrieve a player's details by ID",
                   tags=['General'], response_model=PlayerAPIModel)
async def get_player(id: str):
    player = await fetch_player(id)
    return player
