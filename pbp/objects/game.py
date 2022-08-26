import inspect

import pbp.client as client


class Game(object):
    """
    Class for loading resource data from data loaders with a parent_object of 'Game'
    :param str game_id: Game ID - dependent on resource
    """

    def __init__(self, game_id):
        self.game_id = game_id
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        data_loaders = [a for a in attributes if a[0].endswith(client.DATA_LOADER_SUFFIX)]


game = Game('59159')