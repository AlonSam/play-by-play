from typing import List, Dict

from fastapi import APIRouter, Query, HTTPException

from api.database import fetch_games, fetch_all_players, fetch_teams, fetch_lineups
from api.models import Phase, League
from api.utils import get_seasons, get_phases
from models import GameAPIModel, TeamAPIModel
from models.api.lineup_model import LineupAPIModel

general_router = APIRouter()


@general_router.get("/get-games/{league}", summary="Gets all games by season and phase", response_model=List[GameAPIModel])
async def get_games(league: League, season: str = Query(examples={
        'Single Season': {'value': '2021-22'},
        'Multiple Seasons': {'value': '2020-21,2021-22'}
        }), phase: Phase = Query()
                ):
    seasons = get_seasons(season)
    phases = get_phases(phase)
    games = await fetch_games(league, seasons, phases)
    return games


@general_router.get('/get-all-players/', summary='Gets all players')
async def get_all_players() -> Dict:
    players = await fetch_all_players()
    return players


@general_router.get('/get-players-for-team', summary='Gets all players who played for team in given season(s)')
async def get_players_for_team(team_id: str = Query(example='2'), season: str = Query(examples={
        'Single Season': {'value': '2021-22'},
        'Multiple Seasons': {'value': '2020-21,2021-22'}
        })) -> Dict:
    seasons = get_seasons(season)
    players = await fetch_all_players(team_id, seasons)
    if players:
        return players
    raise HTTPException(status_code=404, detail=f'There exists no team with id: {team_id}')


@general_router.get('/get-teams/{league}', summary='Gets all teams for league and season',
                    response_model=List[TeamAPIModel])
async def get_teams(league: League, season: str = Query(examples={
        'Single Season': {'value': '2021-22'},
        'Multiple Seasons': {'value': '2020-21,2021-22'}
        })):
    seasons = get_seasons(season)
    teams = await fetch_teams(league, seasons)
    if teams:
        return teams
    raise HTTPException(status_code=404, detail='Teams not found')


@general_router.get('/get-lineups-for-team', summary='Gets all combinations of lineups for team in given season(s)',
                    response_model=List[LineupAPIModel])
async def get_lineups_for_team(team_id: str = Query(example='2'), season: str = Query(examples={
        'Single Season': {'value': '2021-22'},
        'Multiple Seasons': {'value': '2020-21,2021-22'}
        })) -> List[LineupAPIModel]:
    seasons = get_seasons(season)
    lineups = await fetch_lineups(team_id, seasons)
    if lineups:
        return lineups
    raise HTTPException(status_code=404, detail='Lineups not found')
