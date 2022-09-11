from pbp.resources.events.field_goal import FieldGoal
from pbp.resources.events.free_throw import FreeThrow


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
            else:
                raise Exception('Rebound after made shot')
        else:
            previous_event = self.previous_event
            while previous_event and not isinstance(previous_event, (FieldGoal, FreeThrow)):
                previous_event = previous_event.previous_event
            if not previous_event.is_made:
                return previous_event
            raise Exception('Missed shot not found')

    @property
    def self_reb(self):
        """
        returns True if rebound was grabbed by the same player who missed the shot, False otherwise
        """
        return self.player_id == self.missed_shot.player_id

    @property
    def is_team_rebound(self):
        return self.team_id == '0'

    @property
    def missed_shot_event_id(self):
        return self.missed_shot.event_id

    @property
    def missed_shot_type(self):
        if isinstance(self.missed_shot, FieldGoal):
            return self.missed_shot.shot_type
        return 'FreeThrow'
