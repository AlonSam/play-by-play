import json

from pbp.data_loader.segev_sports.overrides.overrides_generator import OverridesGenerator

game_id = '35340'
generator = OverridesGenerator(event_id='353400607', period=4, time='08:09', team_id='6')
events = generator.generate_sub(player_in='5092', player_out='1496')
with open(f'{game_id}.json', 'w') as outfile:
    outfile.write(json.dumps(events, indent=4))
