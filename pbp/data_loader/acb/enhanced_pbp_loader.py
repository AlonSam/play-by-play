from pbp.data_loader.acb.pbp_loader import ACBPbpLoader
from pbp.data_loader.enhanced_pbp_loader import EnhancedPbpLoader


class ACBEnhancedPbpLoader(ACBPbpLoader, EnhancedPbpLoader):
    """
    Loads ACB Spanish League enhanced pbp data for game.
    """
    def __init__(self, game_id, source, competition):
        super().__init__(game_id, source, competition)
        self.add_free_throw_count()
        self.link_fastbreak_events()
        self.combine_related_events()
        self.remove_duplicates()

    def link_fastbreak_events(self):
        fgms = [item for item in self.items if 'pt' in item.action_type]
        i = 0
        while i < len(fgms):
            if fgms[i].made and 'fast break' in fgms[i + 1].action_type:
                if fgms[i].player_id == fgms[i + 1].player_id:
                    fgms[i].fastbreak = True
                    self.items.remove(fgms[i + 1])
                    i += 1
            i += 1

    def remove_duplicates(self):
        assists = [item for item in self.items if item.action_type == 'assist']
        for i in range(len(assists) - 1):
            ev = assists[i]
            next_ev = assists[i + 1]
            if ev.player_id == next_ev.player_id:
                if ev.period == next_ev.period and ev.seconds_remaining == next_ev.seconds_remaining:
                    self.items.remove(next_ev)



game_id = '101323'
competition = ['ACB', '2020', 'Regular Season']
pbp_loader = ACBEnhancedPbpLoader(game_id, 'web', competition)