import pbp


class Foul(object):
    """
    class for foul events
    """
    event_type = 'foul'

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
