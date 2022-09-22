from typing import List

import pbp
import pbp.resources.events as e
from models.db.stats_model import StatsModel
from pbp.resources.events import Foul
from pbp.resources.events.segev_sports.event_item import SegevEventItem
from pbp.resources.events.turnover import Turnover

TURNOVER_TYPE_TO_STRING_MAPPER = {
    e.BALL_HANDLING_STRING: pbp.BALL_HANDLING_TURNOVER_STRING,
    e.BAD_PASS_STRING: pbp.BAD_PASS_TURNOVER_STRING,
    e.TRAVEL_STRING: pbp.TRAVELS_STRING,
    e.TWENTY_FOUR_SECOND_STRING: pbp.SHOT_CLOCK_VIOLATION_TURNOVER_STRING,
    e.OFFENSIVE_GOALTENDING_STRING: pbp.OFFENSIVE_GOALTENDING_STRING,
    e.THREE_SECOND_STRING: pbp.THREE_SECOND_VIOLATION_TURNOVER_STRING,
    e.FIVE_SECOND_STRING: pbp.FIVE_SECOND_VIOLATION_TURNOVER_STRING,
    e.EIGHT_SECOND_STRING: pbp.EIGHT_SECOND_VIOLATION_TURNOVER_STRING,
    e.OUT_OF_BOUNDS_STRING: pbp.OUT_OF_BOUNDS_TURNOVER_STRING,
    e.BACKCOURT_STRING: pbp.BACKCOURT_VIOLATION_TURNOVER_STRING,
    e.DOUBLE_DRIBBLE_STRING: pbp.DOUBLE_DRIBBLE_TURNOVER_STRING,
    e.OTHER_STRING: pbp.OTHER_TURNOVER_STRING
}

STEAL_TYPE_TO_STRING_MAPPER = {
    e.BALL_HANDLING_STRING: pbp.BALL_HANDLING_STEAL_STRING,
    e.BAD_PASS_STRING: pbp.BAD_PASS_STEAL_STRING,
    e.OTHER_STRING: pbp.OTHER_STEAL_STRING
}


class SegevTurnover(Turnover, SegevEventItem):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def is_steal(self) -> bool:
        """
        returns True if this is a Live Ball Turnover, False otherwise.
        """
        return hasattr(self, e.STEAL_ID_STRING)

    @property
    def is_bad_pass(self) -> bool:
        return self.sub_type == e.BAD_PASS_STRING

    @property
    def is_ball_handling(self) -> bool:
        return self.sub_type == e.BALL_HANDLING_STRING

    @property
    def is_travel(self) -> bool:
        return self.sub_type == e.TRAVEL_STRING

    @property
    def is_shot_clock_violation(self) -> bool:
        return self.sub_type == e.TWENTY_FOUR_SECOND_STRING

    @property
    def is_offensive_goaltending(self) -> bool:
        return self.sub_type == e.OFFENSIVE_GOALTENDING_STRING

    @property
    def is_3_second_violation(self) -> bool:
        return self.sub_type == e.THREE_SECOND_STRING

    @property
    def is_5_second_violation(self) -> bool:
        return self.sub_type == e.FIVE_SECOND_STRING

    @property
    def is_8_second_violation(self) -> bool:
        return self.sub_type == e.EIGHT_SECOND_STRING

    @property
    def is_out_of_bounds(self) -> bool:
        return self.sub_type == e.OUT_OF_BOUNDS_STRING

    @property
    def is_offensive_foul(self) -> bool:
        return self.sub_type == e.OTHER_STRING and isinstance(self.previous_event, Foul) and self.previous_event.is_offensive_foul

    @property
    def is_backcourt_violation(self) -> bool:
        return self.sub_type == e.BACKCOURT_STRING

    @property
    def is_double_dribble(self) -> bool:
        return self.sub_type == e.DOUBLE_DRIBBLE_STRING

    @property
    def is_unknown(self) -> bool:
        return self.sub_type == e.OTHER_STRING and not self.is_offensive_foul

    @property
    def event_stats(self) -> List[StatsModel]:
        """
        returns list of StatsModel object with all stats for event
        """
        stats_models = []
        team_ids = list(self.players_on_court.keys())
        opponent_team_id = (
            team_ids[0] if self.team_id == team_ids[1] else team_ids[1]
        )
        turnover_keys = []
        steal_keys = []
        if self.is_steal:
            turnover_key = TURNOVER_TYPE_TO_STRING_MAPPER[self.sub_type]
            steal_key = STEAL_TYPE_TO_STRING_MAPPER[self.sub_type]
            live_ball_turnover_key = pbp.LIVEBALL_TURNOVERS_STRING
            turnover_keys.append(live_ball_turnover_key)
            steal_keys.append(steal_key)
            turnover_keys += self._add_misc_stats(turnover_key)
            turnover_keys += self._add_misc_stats(live_ball_turnover_key)
            steal_keys += self._add_misc_stats(steal_key)
        else:
            if self.is_offensive_foul:
                turnover_key = pbp.OFFENSIVE_FOUL_TYPE_STRING
            else:
                turnover_key = TURNOVER_TYPE_TO_STRING_MAPPER[self.sub_type]
            turnover_keys += self._add_misc_stats(turnover_key)
        turnover_keys.append(turnover_key)
        for key in turnover_keys:
            stats_models.append(
                StatsModel(
                    player_id=self.player_id,
                    team_id=self.team_id,
                    stat_key=key,
                    stat_value=1
                )
            )
        for key in steal_keys:
            stats_models.append(
                StatsModel(
                    player_id=getattr(self, e.STEAL_ID_STRING),
                    team_id=opponent_team_id,
                    stat_key=key,
                    stat_value=1
                )
            )
        stats_models = self._add_lineup_data(stats_models)
        return self.base_stats + stats_models