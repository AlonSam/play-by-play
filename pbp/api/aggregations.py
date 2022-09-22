from pprint import pprint

import pandas as pd

from api.database import fetch_possessions_stats_for_instance
from models.api.player_totals_model import PlayerTotalsModel


async def calculate_player_totals(player_id: str) -> PlayerTotalsModel:
    stats = await fetch_possessions_stats_for_instance(player_id, 'player')
    df = pd.DataFrame([stat_model.dict() for stat_model in stats])
    aggregated_stats = dict(df.groupby('stat_key')['stat_value'].sum())
    totals = PlayerTotalsModel(**aggregated_stats)
    pprint(totals.dict())
    return totals



# def stat_mapper(stat_key: str) -> List[str]:
#     stat_keys = []
#     if 'SecondPlayed' in stat_key:
#         stat_keys.append('seconds_played')
#     if 'DefRebounds' in stat_key:
#         stat_keys.append('defensive_rebounds')
#         if '3' in stat_key:
#             stat_keys.append('defensive_three_pt_rebounds')
#         elif 'FreeThrow' in stat_key:
#             stat_keys.append('defensive_ft_rebounds')
#         else:
#             stat_keys.append('defensive_two_pt_rebounds')
#     if 'Made' in stat_key:
#
#     if 'Missed' in stat_key:
#         if '3' in stat_key:
#             stat_keys.append('')

# asyncio.run(calculate_player_totals('2031'))