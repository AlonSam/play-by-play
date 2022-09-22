from typing import List

import pbp
from models.db.stats_model import StatsModel
from pbp.resources.events import FieldGoal
from pbp.resources.events import Foul


class FreeThrow(object):
    """
    Class for free throw events
    """
    event_type = 'freethrow'

    @property
    def is_ft_1_of_1(self):
        return self.sub_type == '1of1'

    @property
    def is_ft_1_of_2(self):
        return self.sub_type == '1of2'

    @property
    def is_ft_2_of_2(self):
        return self.sub_type == '2of2'

    @property
    def is_ft_1_of_3(self):
        return self.sub_type == '1of3'

    @property
    def is_ft_2_of_3(self):
        return self.sub_type == '2of3'

    @property
    def is_ft_3_of_3(self):
        return self.sub_type == '3of3'

    @property
    def is_first_ft(self):
        return self.is_ft_1_of_1 or self.is_ft_1_of_2 or self.is_ft_1_of_3 or '1of' in self.sub_type

    @property
    def is_technical_ft(self):
        return self.foul_that_led_to_ft.is_technical

    @property
    def foul_that_led_to_ft(self):
        event = self
        while event and not isinstance(event, Foul):
            event = event.previous_event
        return event

    @property
    def foul_that_led_to_ft_event_id(self) -> Foul:
        return self.foul_that_led_to_ft.event_id

    @property
    def is_end_ft(self):
        return self.is_ft_1_of_1 or self.is_ft_2_of_2 or self.is_ft_3_of_3

    @property
    def num_ft_for_trip(self):
        if 'of1' in self.sub_type:
            return 1
        if 'of2' in self.sub_type:
            return 2
        if 'of3' in self.sub_type:
            return 3

    @property
    def free_throw_type(self):
        """
        returns a string describing the free throw type
        """
        if self.is_technical_ft:
            return "Technical"
        num_fts = self.num_ft_for_trip
        foul_event = self.foul_that_led_to_ft
        if num_fts == 1:
            if self.foul_that_led_to_ft.is_and_one_foul:
                previous_event = foul_event.previous_event
                while previous_event is not None and not (isinstance(previous_event, FieldGoal) and previous_event.is_made):
                    previous_event = previous_event.previous_event
                if previous_event is not None and isinstance(previous_event, FieldGoal) and previous_event.is_made:
                    and1_shot = previous_event
                    if self.player_id == and1_shot.player_id:
                        return f'{and1_shot.shot_value}ptAnd1'
            return 'Unknown'
        if foul_event.is_unsportsmanlike_foul:
            return pbp.UNSPORTSMANLIKE_FOUL_TYPE_STRING
        if foul_event.is_shooting_foul:
            return f'{num_fts}pt' + pbp.SHOOTING_FOUL_TYPE_STRING
        if self.is_over_the_limit_event:
            return pbp.OVER_THE_LIMIT_STRING + pbp.PERSONAL_FOUL_TYPE_STRING
        return pbp.PERSONAL_FOUL_TYPE_STRING


    @property
    def event_stats(self) -> List[StatsModel]:
        """
        returns list of StatsModel object with all stats for event
        """
        stats_models = []
        stat_keys = []
        if self.is_first_ft or self.is_technical_ft:  # Stats for FT Trip
            free_throw_trip_key = self.free_throw_type + "FreeThrowTrips"
            stat_keys.append(free_throw_trip_key)
            stat_keys += self._add_misc_stats(free_throw_trip_key)
        free_throw_attempt_key = pbp.FREE_THROWS_STRING + pbp.ATTEMPTS_STRING
        stat_keys += self._add_misc_stats(free_throw_attempt_key)
        if self.is_made:
            free_throw_key = pbp.FREE_THROW_STRING + pbp.MAKES_STRING
            stat_keys.append(free_throw_key)
            stat_keys += self._add_misc_stats(free_throw_key)
        for stat_key in stat_keys:
            stats_models.append(
                StatsModel(
                    player_id=self.player_id,
                    team_id=self.team_id,
                    stat_key=stat_key,
                    stat_value=1
                )
            )
        stats_models = self._add_lineup_data(stats_models)
        return self.base_stats + stats_models







