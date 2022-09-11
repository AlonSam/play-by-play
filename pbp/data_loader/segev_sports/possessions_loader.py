import inspect
import json
from pprint import pprint
from typing import List, Type

from pydantic import ValidationError

from pbp.data_loader.possession_loader import PossessionLoader
from pbp.models.events.event_model import EventModel
from pbp.models.events.start_of_period import StartOfPeriodEventModel
from pbp.models.possession_model import PossessionModel
from pbp.resources.possessions.possession_item import PossessionItem


class SegevPossessionLoader(PossessionLoader):

    def __init__(self, events: List[Type[EventModel]]):
        self.events = events
        self.items = []
        events_by_possession = self._split_events_by_possession()
        self.make_possession_items(events_by_possession)
        self.possessions = []
        for item in self.items:
            try:
                possession = PossessionModel(**self.get_attributes(item))
            except ValidationError as e:
                print(e)
                pprint(self.get_attributes(item))
                break
            self.possessions.append(possession)
        # self.possessions = [PossessionModel(**self.get_attributes(item)) for item in self.items]

    def make_possession_items(self, events_by_possession):
        for i, possession_events in enumerate(events_by_possession):
            possession = PossessionItem(possession_events)
            possession.possession_id = f'{possession.game_id}{i + 1:03d}'
            if i > 0:
                previous_possession = self.items[i - 1]
            period_start = any(isinstance(event, StartOfPeriodEventModel) for event in possession.events)
            if period_start or i == 0:
                possession.previous_possession = None
                possession.previous_possession_id = None
                if i != 0:
                    previous_possession.next_possession = None
                    previous_possession.next_possession_id = None
            else:
                possession.previous_possession = previous_possession
                possession.previous_possession_id = previous_possession.possession_id
                previous_possession.next_possession = possession
                previous_possession.next_possession_id = possession.possession_id
                if i == len(events_by_possession) - 1:
                    possession.next_possession = None
                    possession.next_possession_id = None
            self.items.append(possession)

    @staticmethod
    def get_attributes(item):
        attributes = dict(inspect.getmembers(item, lambda a: not (inspect.isroutine(a))))
        return {k: v for (k, v) in attributes.items() if not (k.startswith('__') and k.endswith('__'))}

    def _save_data_to_file(self):
        with open('possessions.json', 'w') as outfile:
            json.dump(self.export_data, outfile, indent=4)
