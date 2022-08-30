from pbp.data_loader.enhanced_pbp_loader import EnhancedPbpLoader
from pbp.data_loader.segev_sports.details.loader import SegevDetailsLoader
from pbp.data_loader.segev_sports.pbp.loader import SegevPbpLoader
from pbp.resources.enhanced_pbp import FreeThrow, FieldGoal, Turnover, Rebound, Foul, StartOfPeriod, Substitution
from pbp.resources.enhanced_pbp.segev_sports.enhanced_pbp_factory import SegevEnhancedPbpFactory


def _load_team_ids(game_id):
    details = SegevDetailsLoader.from_db(game_id).item
    return str(details.home_id), str(details.away_id)


class SegevEnhancedPbpLoader(SegevPbpLoader, EnhancedPbpLoader):
    """
    Loads Segev Sports enhanced pbp data for game.
    """

    data_provider = 'segev_sports'
    resource = 'enhancedpbp'
    parent_object = 'Game'

    def __init__(self, game_id):
        super().__init__(game_id)
        self.game_id = game_id
        self._make_enhanced_pbp_items()

    def _make_enhanced_pbp_items(self):
        self.factory = SegevEnhancedPbpFactory()
        self._combine_related_events()
        self.items = [self.factory.get_event_class(item['action_type'])(**item) for item in self.data]
        self._add_extra_attrs_to_all_events()

    def _set_period_starters(self):
        for i in self.start_period_indices:
            self.items[i].period_starters = self.items[i].get_period_starters()

    def _combine_related_events(self):
        subs_to_remove = []
        for i, event in enumerate(self.items):
            actions = {'turnover': 'steal', 'foul': 'foul_on',
                       '2pt': ['assist', 'block'], '3pt': ['assist', 'block'],
                       'freethrow': 'assist'}
            if event.action_type in actions:
                related = self.get_related_events(i)
                for ev in related:
                    if 'pt' in event.action_type:
                        for act in actions[event.action_type]:
                            if act == ev.action_type:
                                act += '_player_id'
                                setattr(event, act, ev.player_id)
                                self.items.remove(ev)
                        if event.is_made and ev.action_type == 'foul':
                            ev.sub_type = 'and_one'
                    elif actions[event.action_type] == ev.action_type:
                        act = ev.action_type + "_player_id"
                        setattr(event, act, ev.player_id)
                        if event.action_type == 'freethrow' and event.sub_type.split('of')[0] == '1':
                            for ft in related:
                                if ft.action_type == 'freethrow':
                                    setattr(ft, act, ev.player_id)
                        self.items.remove(ev)
            elif event.action_type == 'substitution':
                if not hasattr(event, 'sub_type') or event in subs_to_remove:
                    continue
                if event.sub_type == 'in' and event.period == 1 and event.seconds_remaining == 600:
                    event.sub_in_player_id = event.player_id
                    continue
                try:
                    subs_to_remove += self.pair_subs_at_current_time(i)
                except:
                    print(event)
        for sub in subs_to_remove:
            self.items.remove(sub)

    def _add_score_and_margin_to_all_events(self):
        self.home_id, self.away_id = _load_team_ids(self.game_id)
        if self.items[0].score is not None and isinstance(self.items[0].score, dict):
            return
        score = {self.home_id: 0, self.away_id: 0}
        for i, event in enumerate(self.items):
            if hasattr(event, 'score') and event.score:
                away_score, home_score = event.score.split('-')
                score[self.home_id] = int(home_score)
                score[self.away_id] = int(away_score)
            event.score = score.copy()
            if event.offense_team_id == self.home_id or event.team_id == 0:
                event.margin = event.score[self.home_id] - event.score[self.away_id]
            else:
                event.margin = event.score[self.away_id] - event.score[self.home_id]

    def _add_offense_team_id_to_all_events(self):
        for i, event in enumerate(self.items):
            if isinstance(event, StartOfPeriod):
                event.offense_team_id = self.get_period_first_offense_team_id(event)
            else:
                event.offense_team_id = self.get_offense_team_id(event)

    def get_offense_team_id(self, event):
        offensive_actions = (FieldGoal, FreeThrow, Turnover)
        team_id = event.team_id
        if isinstance(event, offensive_actions):
            offense_team_id = team_id
        elif isinstance(event, Rebound):
            offense_team_id = team_id if event.is_offensive else self.get_other_id(team_id)
        elif isinstance(event, Foul):
            offense_team_id = team_id if event.is_offensive_foul else self.get_other_id(team_id)
        else:
            offense_team_id = event.previous_event.offense_team_id
        return offense_team_id

    def get_period_first_offense_team_id(self, event):
        event = event.next_event
        while event and isinstance(event, (Substitution, StartOfPeriod)):
            event = event.next_event
        return self.get_offense_team_id(event)

    def get_other_id(self, id):
        if id == int(self.home_id):
            return int(self.away_id)
        return int(self.home_id)

    @property
    def data(self):
        return [item if isinstance(item, dict) else item.dict() for item in self.items]

    @property
    def export_data(self):
        return [item.export_data for item in self.items]