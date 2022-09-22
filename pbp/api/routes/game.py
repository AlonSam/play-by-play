from __future__ import annotations

from fastapi import APIRouter

from api.database import (
    fetch_shots_for_instance
)

game_router = APIRouter()





@game_router.get("/get-game-shots/{id}", summary="Retrieve all shots taken by instance")
async def get_shots(id: str):
    shots = await fetch_shots_for_instance(id, 'game')
    if shots:
        return shots


@game_router.get('/get-games-shots/{ids}')
async def get_game_shots(ids: str):
    id_list = ids.split(',')
    shots = []
    for id in id_list:
        shots += await fetch_shots_for_instance(id, 'game')
    return shots
