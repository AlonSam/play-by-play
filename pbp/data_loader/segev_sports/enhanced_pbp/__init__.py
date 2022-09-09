from pbp.models.events.deflection import DeflectionEvent
from pbp.models.events.end_of_period import EndOfPeriodEvent
from pbp.models.events.field_goal import FieldGoalEvent
from pbp.models.events.foul import FoulEvent
from pbp.models.events.free_throw import FreeThrowEvent
from pbp.models.events.rebound import ReboundEvent
from pbp.models.events.start_of_period import StartOfPeriodEvent
from pbp.models.events.substitution import SubstitutionEvent
from pbp.models.events.timeout import TimeoutEvent
from pbp.models.events.turnover import TurnoverEvent
from pbp.resources.enhanced_pbp.segev_sports import *

SUBSTITUTION_STRING = 'substitution'
TWO_POINT_STRING = '2pt'
THREE_POINT_STRING = '3pt'
START_OF_PERIOD_STRING = 'startofperiod'
FOUL_STRING = 'foul'
ASSIST_STRING = 'assist'
TURNOVER_STRING = 'turnover'
FT_STRING = 'freethrow'
STEAL_STRING = 'steal'
BLOCK_STRING = 'block'
BLOCKED_STRING = 'blocked'
FOUL_ON_STRING = 'foul_on'
SUBSTITUTION_OUT_STRING = 'out'
SUBSTITUTION_IN_STRING = 'in'
REBOUND_STRING = 'rebound'
OFFENSIVE_STRING = 'offensive'
DEFENSIVE_STRING = 'defensive'

OBJECT_MAPPER = {
    SegevRebound: ReboundEvent,
    SegevFoul: FoulEvent,
    SegevFieldGoal: FieldGoalEvent,
    SegevStartOfPeriod: StartOfPeriodEvent,
    SegevSubstitution: SubstitutionEvent,
    SegevDeflection: DeflectionEvent,
    SegevTimeout: TimeoutEvent,
    SegevTurnover: TurnoverEvent,
    SegevFreeThrow: FreeThrowEvent,
    SegevEndOfPeriod: EndOfPeriodEvent
}