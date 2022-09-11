from pbp.data_loader.event_loader import EventLoader
from pbp.data_loader.fiba.pbp_loader import FibaPbpLoader


class FibaEnhancedPbpLoader(FibaPbpLoader, EventLoader):
    """
    Loads FIBA Live Stats enhanced pbp data for game.
    """
    def __init__(self, game_id, source, competition):
        super().__init__(game_id, source, competition)
        self.combine_related_events()
        for item in self.items:
            print(item.data)

    def combine_related_events(self):
        for i, event in enumerate(self.items):
            actions = {'turnover': 'steal', 'foul': 'foulon', '2pt': ['assist', 'block'], '3pt': ['assist', 'block'],
                       'freethrow': 'assist'}
            if event.action_type in actions:
                related = self.get_related_events(i)
                for ev in related:
                    if 'pt' in event.action_type:
                        for act in actions[event.action_type]:
                            if act == ev.action_type:
                                setattr(event, act, ev.player_id)
                                self.items.remove(ev)
                    elif actions[event.action_type] == ev.action_type:
                        setattr(event, ev.action_type, ev.player_id)
                        self.items.remove(ev)
            elif event.action_type == 'substitution':
                if event.sub_type == 'in':
                    self.event_within_5_seconds(event, i, 'out')
                    if not hasattr(event, 'sub_out'):
                        raise Exception('Substitution in has no related event')
                    event.sub_in = event.player_id
                else:
                    self.event_within_5_seconds(event, i, 'in')
                    if not hasattr(event, 'sub_in'):
                        raise Exception('Substitution out has no related event')
                    event.sub_out = event.player_id
                delattr(event, 'player')
                delattr(event, 'player_id')
                delattr(event, 'num')
                event.sub_type = ''




game_id = '1758418'
competition = ['Champions League', '2020', 'Qualifiers']
pbp_loader = FibaEnhancedPbpLoader(game_id, 'web', competition)