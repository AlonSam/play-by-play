from __future__ import annotations

from typing import List, Dict

import motor.motor_asyncio

from api.models import League
from models import *
from models.api.lineup_model import LineupAPIModel
from models.api.shot_model import ShotModel

MONGO_DETAILS = "mongodb://localhost:27017"
motor_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = motor_client.PBP
games_collection = database.get_collection('games')
possessions_collection = database.get_collection('possessions')
players_collection = database.get_collection('players')
teams_collection = database.get_collection('teams')
lineups_collection = database.get_collection('lineups')

ENTITY_TO_COLLECTION_MAPPER = {
    'player': players_collection,
    'team': teams_collection,
    'game': games_collection,
    'lineup': lineups_collection
}


def create_player(player: dict, team_name: str) -> PlayerAPIModel:
    return PlayerAPIModel(id=player['_id'], name=player['name'], hebrew_name=player['hebrewName'], team_name=team_name)


def create_game(game: dict, home_possessions: int, away_possessions: int) -> GameAPIModel:
    details = game['details']
    return GameAPIModel(
        game_id=game['_id'],
        basket_id=details['basketId'],
        date=details['time'].date(),
        home_team_id=details['homeId'],
        away_team_id=details['awayId'],
        home_team_name=details['homeTeam'],
        away_team_name=details['awayTeam'],
        home_score=details['homeScore'],
        away_score=details['awayScore'],
        home_possessions=home_possessions,
        away_possessions=away_possessions
    )


async def fetch_player(id: str) -> PlayerAPIModel:
    player = await players_collection.find_one({'_id': id}, {'name': 1, 'hebrewName': 1, 'teamId': 1})
    if player:
        team = await fetch_team(player['teamId'])
        team_name = team.name
        return create_player(player, team_name)


async def fetch_all_players(team_id: str = None, seasons: List[str] = None) -> Dict:
    players = {}
    if team_id is not None:
        for season in seasons:
            cursor = players_collection.find({f'team_ids.{season}': team_id})
            async for document in cursor:
                players[document['_id']] = document['name']
    else:
        cursor = players_collection.find({})
        async for document in cursor:
            players[document['_id']] = document['name']
    return players


async def fetch_team(id: str) -> TeamAPIModel:
    team = await teams_collection.find_one({'_id': id}, {'name': 1})
    if team:
        return TeamAPIModel(id=team['_id'], name=team['name'])


async def fetch_teams(league: League, seasons: List[str]):
    teams = []
    for season in seasons:
        cursor = teams_collection.find({'seasons': {'$in': seasons}})
        async for document in cursor:
            teams.append(TeamAPIModel(id=document['_id'], name=document['name']))
    return teams


async def fetch_game(id: str) -> GameModel:
    game = await games_collection.find_one({'_id': id})
    if game:
        return GameModel(**game)


async def fetch_game_for_api(id: str):
    game = await games_collection.find_one({'_id': id}, {'details': 1, 'possessions': 1})
    home_possessions = await get_offensive_possession_ids_for_team(game_id=id, team_id=game['details']['homeId'])
    away_possessions = await get_offensive_possession_ids_for_team(game_id=id, team_id=game['details']['awayId'])
    if game:
        return create_game(game, home_possessions, away_possessions)


async def fetch_games(league: League, seasons: List[str], phases: List[str]) -> List[PlayerAPIModel]:
    query = {'details.competition': league,
             'details.season': {
                 '$in': seasons
                },
             'details.phase': {
                 '$in': phases
                }
             }
    cursor = games_collection.find(query)
    games = []
    async for document in cursor:
        home_possessions = await get_offensive_possession_ids_for_team(game_id=document['_id'], team_id=document['details']['homeId'])
        away_possessions = await get_offensive_possession_ids_for_team(game_id=document['_id'], team_id=document['details']['awayId'])
        games.append(create_game(document, home_possessions, away_possessions))
    return games


async def fetch_lineups(team_id: str, seasons: List[str]) -> List[LineupAPIModel]:
    query = {'teamId': team_id}
    cursor = lineups_collection.find(query)
    lineups = []
    async for document in cursor:
        lineup = LineupModel(**document)
        team = await fetch_team(lineup.team_id)
        players = []
        for player_id in lineup.player_ids:
            player = await fetch_player(player_id)
            players.append(player.name)
        lineups.append(LineupAPIModel(id=lineup.id, team_name=team.name, team_id=team.id,
                                      players=", ".join(players)))
    return lineups


async def get_offensive_possession_ids_for_team(game_id: str, team_id: str):
    query = {'_id': team_id}
    team = await teams_collection.find_one(query, {'possessions': 1})
    possessions = []
    if team:
        possessions = [possession_id for possession_id in team['possessions']['offense'] if
                       possession_id.startswith(game_id)]
    return len(possessions)


async def fetch_players_for_team(team_id: str) -> List[PlayerAPIModel]:
    team = await fetch_team(team_id)
    players = []
    async for player in players_collection.find({'teamId': team_id}):
        players.append(create_player(player, team.name))
    return players


async def fetch_offensive_possessions_for_instance(id: str, entity_str: str) -> List[PossessionModel]:
    collection = ENTITY_TO_COLLECTION_MAPPER[entity_str]
    entity = await collection.find_one({'_id': id}, {'possessions': 1})
    offensive_possessions = entity['possessions']['offense']
    possessions = []
    for possession_id in offensive_possessions:
        possession = await possessions_collection.find_one({'_id': possession_id})
        possessions.append(PossessionModel(**possession))
    return possessions


async def fetch_possessions_for_instance(id: str, instance_str: str) -> list[PossessionModel]:
    collection = ENTITY_TO_COLLECTION_MAPPER[instance_str]
    instance = await collection.find_one({'_id': id}, {'possessions': 1})
    possessions = []
    for possession_ids in instance['possessions'].values():
        for possession_id in possession_ids:
            possession = await possessions_collection.find_one({'_id': possession_id})
            possessions.append(PossessionModel(**possession))
    return possessions


async def fetch_possessions_stats_for_instance(id: str, instance_str: str):
    possessions = await fetch_possessions_for_instance(id, instance_str)
    return [stat_model for possession in possessions for stat_model in possession.possession_stats if getattr(stat_model, f'{instance_str}_id') == id]


async def fetch_shots_for_instance(id: str, entity_str: str, season: str, phases: List[str]) -> List[ShotModel]:
    collection = ENTITY_TO_COLLECTION_MAPPER[entity_str]
    entity = await collection.find_one({'_id': id}, {'possessions': 1, 'games': 1})
    games = entity['games']
    filtered_games = []
    for game_id in games:
        query = {'_id': game_id,
                 'details.season': season,
                 'details.phase': {'$in': phases}
                 }
        game = await games_collection.find_one(query)
        if game:
            filtered_games.append(game_id)
    offensive_possessions = [possession_id for possession_id in entity['possessions']['offense'] if possession_id[:5] in filtered_games]
    shots = []
    for possession_id in offensive_possessions:
        query = {'_id': possession_id, f'events.{entity_str}Id': id, 'events.actionType': {'$in': ['2pt', '3pt']}}
        possession_dict = await possessions_collection.find_one(query)
        if possession_dict:
            possession = PossessionModel(**possession_dict)
            opponent_team_id = possession.defense_team_id
            lineup_id = possession.offense_lineup_id
            opponent_lineup_id = possession.defense_lineup_id
            for event in possession.events:
                if isinstance(event, FieldGoalEventModel):
                    shots.append(
                        ShotModel(
                            event_id=event.event_id,
                            player_id=event.player_id,
                            team_id=event.team_id,
                            opponent_team_id=opponent_team_id,
                            lineup_id=lineup_id,
                            opponent_lineup_id=opponent_lineup_id,
                            made=event.is_made,
                            x=event.x,
                            y=event.y,
                            time=event.seconds_remaining,
                            shot_value=event.shot_value,
                            is_putback=event.is_putback,
                            shot_zone=event.shot_zone,
                            basic_shot_zone=event.basic_shot_zone,
                            margin=event.margin,
                            is_and_one=event.is_and_one,
                            is_assisted=event.is_assisted,
                            assist_player_id=event.assist_player_id,
                            is_blocked=event.is_blocked,
                            block_player_id=event.block_player_id
                        )
                    )
    return shots
