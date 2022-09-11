import inspect
from collections import defaultdict
from typing import List, Dict, Type

from pbp.data_loader.event_loader import EventLoader
from pbp.models.events.deflection import DeflectionEventModel
from pbp.models.events.end_of_period import EndOfPeriodEventModel
from pbp.models.events.field_goal import FieldGoalEventModel
from pbp.models.events.foul import FoulEventModel
from pbp.models.events.free_throw import FreeThrowEventModel
from pbp.models.events.rebound import ReboundEventModel
from pbp.models.events.start_of_period import StartOfPeriodEventModel
from pbp.models.events.substitution import SubstitutionEventModel
from pbp.models.events.timeout import TimeoutEventModel
from pbp.models.events.turnover import TurnoverEventModel
from pbp.resources.events.segev_sports import *
from pbp.resources.events.segev_sports.event_item import SegevEventItem
from pbp.resources.events.segev_sports.events_factory import SegevEventsFactory
from pbp.resources.pbp.segev_pbp_item import SegevPbpItem

SUBSTITUTION_STRING = 'substitution'
TWO_POINT_STRING = '2pt'
THREE_POINT_STRING = '3pt'
START_OF_PERIOD_STRING = 'startofperiod'
FOUL_STRING = 'foul'
ASSIST_STRING = 'assist'
TURNOVER_STRING = 'turnover'
FT_STRING = 'freethrow'
STEAL_STRING = 'steal'
AND_ONE_STRING = 'and_one'
BLOCK_STRING = 'block'
BLOCKED_STRING = 'blocked'
FOUL_ON_STRING = 'foul_on'
SUBSTITUTION_OUT_STRING = 'out'
SUBSTITUTION_IN_STRING = 'in'
REBOUND_STRING = 'rebound'
OFFENSIVE_STRING = 'offensive'
DEFENSIVE_STRING = 'defensive'
DEFLECTION_STRING = 'deflection'

OBJECT_MAPPER = {
    SegevRebound: ReboundEventModel,
    SegevFoul: FoulEventModel,
    SegevFieldGoal: FieldGoalEventModel,
    SegevStartOfPeriod: StartOfPeriodEventModel,
    SegevSubstitution: SubstitutionEventModel,
    SegevDeflection: DeflectionEventModel,
    SegevTimeout: TimeoutEventModel,
    SegevTurnover: TurnoverEventModel,
    SegevFreeThrow: FreeThrowEventModel,
    SegevEndOfPeriod: EndOfPeriodEventModel
}

class SegevEventLoader(EventLoader):
    """
    Loads Segev Sports enhanced pbp data for game.
    """

    def __init__(self, game_id: str, raw_events: List[SegevPbpItem], home_id: str, away_id: str):
        self.game_id = game_id
        self.raw_events = raw_events
        self.home_id = home_id
        self.away_id = away_id
        self.items = []
        self._make_enhanced_pbp_items()
        self.events = [OBJECT_MAPPER[type(item)](**self.get_attributes(item)) for item in self.items]

    def _make_enhanced_pbp_items(self):
        self.factory = SegevEventsFactory()
        self.combined_events = self._combine_related_events()
        fouls_to_give = defaultdict(lambda: 4)
        player_game_fouls = defaultdict(int)
        for i, combined_event in enumerate(self.combined_events):
            event = self.factory.get_event_class(combined_event.action_type)(combined_event)
            event.game_id = self.game_id
            if i > 0:
                previous_event = self.items[i - 1]
            if isinstance(event, SegevStartOfPeriod) or i == 0:
                if i != 0:
                    event.previous_event = previous_event
                    event.previous_event_id = previous_event.event_id
                    previous_event.next_event = None
                    previous_event.next_event_id = None
                else:
                    event.previous_event = None
                    event.previous_event_id = None
                event.offense_team_id = self.get_period_first_offense_team_id(i + 1)
                event.period_starters = self._get_period_starters(i + 1, event)
                if event.period <= 4:
                    fouls_to_give = defaultdict(lambda: 4)
            else:
                event.offense_team_id = self.get_offense_team_id(combined_event)
                event.previous_event = previous_event
                event.previous_event_id = previous_event.event_id
                previous_event.next_event = event
                previous_event.next_event_id = event.event_id
                if i == len(self.combined_events) - 1:
                    event.next_event = None
                    event.next_event_id = None
            if isinstance(event, SegevFoul):
                if event.counts_towards_penalty and fouls_to_give[event.team_id] > 0:
                    fouls_to_give[event.team_id] -= 1
                if event.counts_as_personal_foul:
                    player_game_fouls[event.player_id] += 1
            event.fouls_to_give = fouls_to_give.copy()
            event.player_game_fouls = player_game_fouls.copy()
            event.score = self._get_score(event)
            event.margin = self._get_margin(event)
            self.items.append(event)

    @staticmethod
    def get_attributes(item):
        attributes = dict(inspect.getmembers(item, lambda a: not (inspect.isroutine(a))))
        return {k: v for (k, v) in attributes.items() if not (k.startswith('__') and k.endswith('__'))}

    def _get_period_starters(self, i: int, event: Type[SegevEventItem]) -> Dict:
        if event.period == 1:
            starters = {}
        else:
            starters = event.previous_event.players_on_court
        combined_event = self.combined_events[i]
        while combined_event and combined_event.action_type == SUBSTITUTION_STRING:
            if combined_event.team_id not in starters.keys():
                starters[combined_event.team_id] = []
            if hasattr(combined_event, 'sub_out_player_id'):
                if combined_event.sub_out_player_id in starters[combined_event.team_id]:
                    starters[combined_event.team_id].remove(combined_event.sub_out_player_id)
            starters[combined_event.team_id].append(combined_event.sub_in_player_id)
            i += 1
            combined_event = self.combined_events[i]
        return starters

    def _combine_related_events(self):
        actions_to_skip = [STEAL_STRING, FOUL_ON_STRING, ASSIST_STRING, BLOCK_STRING]
        events_to_skip = []
        combined_events = []
        for i, event in enumerate(self.raw_events):
            if event.action_type in actions_to_skip: continue
            if event in events_to_skip:
                events_to_skip.remove(event)
                continue
            actions = {TURNOVER_STRING: STEAL_STRING, FOUL_STRING: FOUL_ON_STRING,
                       TWO_POINT_STRING: [ASSIST_STRING, BLOCK_STRING], THREE_POINT_STRING: [ASSIST_STRING, BLOCK_STRING],
                       FT_STRING: ASSIST_STRING}
            if event.action_type in actions:
                related = self.get_related_events(i)
                for ev in related:
                    if 'pt' in event.action_type:
                        for act in actions[event.action_type]:
                            if act == ev.action_type:
                                act += '_player_id'
                                setattr(event, act, ev.player_id)
                                events_to_skip.append(ev)
                        if event.is_made and ev.action_type == FOUL_STRING:
                            ev.sub_type = AND_ONE_STRING
                    elif actions[event.action_type] == ev.action_type:
                        act = ev.action_type + "_player_id"
                        setattr(event, act, ev.player_id)
                        if event.action_type == FT_STRING and event.sub_type.split('of')[0] == '1':
                            for ft in related:
                                if ft.action_type == FT_STRING:
                                    setattr(ft, act, ev.player_id)
                        events_to_skip.append(ev)
            elif event.action_type == SUBSTITUTION_STRING:
                combined_subs, subs_to_skip = self.pair_subs_at_current_time(i)
                combined_events += combined_subs
                events_to_skip += subs_to_skip
                continue
                # if event.period == 1 and event.seconds_remaining == 600 and hasattr(event, 'sub_type'):
                #     if event.sub_type == 'in':
                #         event.sub_in_player_id = event.player_id
                #         delattr(event, 'player_id')
                #         delattr(event, 'sub_type')
                #     else:
                #         combined_subs, subs_to_skip = self.pair_subs_at_current_time(i)
                #         combined_events += combined_subs
                #         events_to_skip += subs_to_skip
                #         continue
                # elif hasattr(event, 'sub_type'):
                #     combined_subs, subs_to_skip = self.pair_subs_at_current_time(i)
                #     combined_events += combined_subs
                #     events_to_skip += subs_to_skip
                #     continue
            combined_events.append(event)
        return combined_events

    def _get_score(self, event: Type[SegevEventItem]) -> Dict:
        if event.previous_event:
            score = event.previous_event.score
        else:
            score = {self.home_id: 0, self.away_id: 0}
        if hasattr(event, 'score'):
            away_score, home_score = event.score.split('-')
            score[self.home_id] = int(home_score)
            score[self.away_id] = int(away_score)
        return score.copy()

    def _get_margin(self, event: Type[SegevEventItem]) -> int:
        margin = event.score[self.home_id] - event.score[self.away_id]
        if event.offense_team_id == self.home_id or event.team_id == 0:
            return margin
        else:
            return margin * -1

    def get_offense_team_id(self, event: SegevPbpItem) -> str:
        offensive_actions = (TWO_POINT_STRING, THREE_POINT_STRING, FT_STRING, TURNOVER_STRING)
        team_id = event.team_id
        if event.action_type in offensive_actions:
            return team_id
        elif event.action_type == REBOUND_STRING or event.action_type == FOUL_STRING:
            return team_id if event.sub_type == OFFENSIVE_STRING else self.get_other_id(team_id)
        elif event.action_type == DEFLECTION_STRING:
            return self.get_other_id(team_id)
        return self.items[-1].offense_team_id

    def get_period_first_offense_team_id(self, i: int) -> str:
        event = self.combined_events[i]
        while event and (event.action_type == SUBSTITUTION_STRING or event.action_type == START_OF_PERIOD_STRING):
            i += 1
            event = self.combined_events[i]
        return self.get_offense_team_id(event)

    def get_other_id(self, team_id: str) -> str:
        return self.away_id if team_id == self.home_id else self.home_id

    @property
    def data(self) -> List[Dict]:
        return [item if isinstance(item, dict) else item.dict() for item in self.items]

    @property
    def export_data(self) -> List[Dict]:
        return [item.export_data for item in self.items]
