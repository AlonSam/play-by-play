import pbp.resources.events as e
from pbp.resources.events import Foul
from pbp.resources.events.segev_sports.event_item import SegevEventItem
from pbp.resources.events.turnover import Turnover


class SegevTurnover(Turnover, SegevEventItem):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def is_steal(self) -> bool:
        """
        returns True if this is a Live Ball Turnover, False otherwise.
        :return:
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
    def is_lane_violation(self) -> bool:
        return self.sub_type == e.LANE_VIOLATION_STRING

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
