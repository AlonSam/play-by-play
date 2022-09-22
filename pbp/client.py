from __future__ import annotations

from pydantic import ValidationError

from game_loader import GameLoader


class Client:
    def __init__(self, game_ids: list[str]):
        self.game_ids = game_ids

    def load_games(self):
        saved = []
        for game_id in self.game_ids[:30]:
            if game_id in saved:
                continue
            game_loader = GameLoader(game_id)
            try:
                game_loader.load_game()
            except ValidationError as e:
                print(e)
                print(game_id)
                print(saved)
                break
            except Exception as e:
                print(f'{type(e).__name__}: {e}')
                print(game_id)
                print(saved)
                break
            saved.append(game_id)
            print(game_id)

game_ids = []
with open('game_ids.txt', 'r') as outfile:
    for line in outfile:
        game_id = str(line[:-1])
        game_ids.append(game_id)

client = Client(game_ids)
# client = Client(['24674'])
client.load_games()