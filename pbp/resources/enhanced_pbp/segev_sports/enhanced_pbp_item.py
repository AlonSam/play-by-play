from typing import Optional, Dict, Union

from pbp.resources.enhanced_pbp import StartOfPeriod
from pbp.resources.enhanced_pbp.enhanced_pbp_item import EnhancedPbpItem


class SegevEnhancedPbpItem(EnhancedPbpItem):
    """
    Base class for enhanced pbp events from Segev Sports
    """
    event_id: int
    game_id: Optional[int]
    parent_event_id: int
    action_type: str
    sub_type: Optional[str]
    player_id: Optional[int]
    team_id: int
    period: int
    time: str
    seconds_remaining: int
    score: Optional[Union[str, dict]]
    is_fastbreak: Optional[bool]
    is_from_turnover: Optional[bool]
    is_second_chance: Optional[bool]
    fouls_to_give: Optional[Dict]
    player_game_fouls: Optional[Dict]
    offense_team_id: Optional[int]

    @property
    def is_possession_ending_event(self):
        """
        returns True if event ends a possession, False otherwise
        """
        if self.next_event is None:
            return True
        if isinstance(self, StartOfPeriod):
            return False
        return self.offense_team_id != self.next_event.offense_team_id

    def get_all_related_events(self):
        """
        returns list of all directly related events to current event
        """
        events = [self]
        prev_id = self.previous_event_id
        if len(prev_id) == 0:
            # Check only forwards
            next_event = self.next_event
            while next_event and (next_event.event_id == prev_id or next_event.previous_event_id == prev_id):
                events.append(next_event)
                next_event = next_event.next_event
        # Check backwards
        prev_event = self.previous_event
        while prev_event and (prev_event.event_id == prev_id or prev_event.previous_event_id == prev_id):
            events.append(prev_event)
            prev_event = prev_event.previous_event
        return events