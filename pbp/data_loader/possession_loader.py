from pbp.resources.enhanced_pbp import StartOfPeriod


class PossessionLoader(object):
    """
    Class for shared methods between :obj:`~pbpstats.data_loader.segev_sports.possessions_loader.SegevPossessionLoader`,
    :obj:`~pbpstats.data_loader.fiba.possessions_loader.FibaPossessionLoader`
    :obj:`~pbpstats.data_loader.euroleague.possessions_loader.ELPossessionLoader`
    and :obj:`~pbpstats.data_loader.acb.possessions_loader.ACBPossessionLoader`
    All above should inherit from this class.
    This class should not be instantiated directly
    """

    def _split_events_by_possession(self):
        """
        splits events by possession
        :returns: list of lists with events for each possession
        """
        events = []
        possession_events = []
        for event in self.events:
            possession_events.append(event)
            if event.is_possession_ending_event:
                events.append(possession_events)
                possession_events = []
        return events

    def _add_extra_attrs_to_all_possessions(self):
        """
        adds possession id and next and previous possession to each possession
        """
        for i, possession in enumerate(self.items):
            period_start = any(isinstance(event, StartOfPeriod) for event in possession.events)
            if i == 0 and i == len(self.items) - 1:
                possession.previous_possession = None
                possession.next_possession = None
            elif period_start or i == 0:
                possession.previous_possession = None
                possession.next_possession = self.items[i + 1]
            elif i == len(self.items) - 1 or possession.period != self.items[i + 1].period:
                possession.previous_possession = self.items[i - 1]
                possession.next_possession = None
            else:
                possession.previous_possession = self.items[i - 1]
                possession.next_possession = self.items[i + 1]
            possession.possession_id = i + 1