from pbp.resources.enhanced_pbp import (
    FieldGoal,
    FreeThrow,
)


class Rebound(object):
    """
    class for Rebound events
    """
    event_type = 'rebound'

    @property
    def missed_shot(self):
        """
        returns FieldGoal or FreeThrow object for shot that was missed
        """
        if isinstance(self.previous_event, (FieldGoal, FreeThrow)):
            if not self.previous_event.is_made:
                return self.previous_event
        raise Exception(f'{self.previous_event} is not a missed shot')

    @property
    def self_reb(self):
        """
        returns True if rebound was grabbed by the same player who missed the shot, False otherwise
        """
        return self.player_id == self.missed_shot.player_id

    @property
    def is_defensive(self):
        return self.sub_type == 'defensive'

    @property
    def is_offensive(self):
        return self.sub_type == "offensive"