from pbp.resources.enhanced_pbp import Foul


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
    def foul_that_led_to_ft_event_id(self):
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

