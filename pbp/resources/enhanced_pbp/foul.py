import pbp
import pbp.resources.enhanced_pbp as e


class Foul(object):
    """
    class for foul events
    """
    event_type = 'foul'
    @property
    def is_personal_foul(self):
        return self.sub_type == e.PERSONAL_STRING

    @property
    def is_shooting_foul(self):
        return self.sub_type == e.SHOOTING_STRING or self.sub_type == e.AND_ONE_STRING

    @property
    def is_offensive_foul(self):
        return self.sub_type == e.OFFENSIVE_STRING

    @property
    def is_and_one_foul(self):
        return self.sub_type == e.AND_ONE_STRING

    @property
    def is_technical(self):
        return self.sub_type == e.TECHNICAL_STRING

    @property
    def is_unsportsmanlike_foul(self):
        return self.sub_type == e.UNSPORTSMANLIKE_STRING

    @property
    def counts_towards_penalty(self):
        return not self.is_technical

    @property
    def counts_as_personal_foul(self):
        """
        TODO: In case of coach/bench technical.
        """
        return not self.is_technical

    @property
    def foul_type_string(self):
        if self.is_personal_foul:
            return pbp.PERSONAL_FOUL_TYPE_STRING
        if self.is_shooting_foul:
            return pbp.SHOOTING_FOUL_TYPE_STRING
        if self.is_offensive_foul:
            return pbp.OFFENSIVE_FOUL_TYPE_STRING
        if self.is_technical:
            return pbp.TECHNICAL_FOUL_TYPE_STRING
        if self.is_unsportsmanlike_foul:
            return pbp.UNSPORTSMANLIKE_FOUL_TYPE_STRING
