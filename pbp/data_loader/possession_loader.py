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