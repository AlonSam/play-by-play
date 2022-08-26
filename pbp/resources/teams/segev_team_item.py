class SegevTeamItem(object):
    """
    class for team data from Segev Sports

    :param dict item: dict with team data
    """
    competitions = []

    def __init__(self, id, name, competition):
        self.id = int(id)
        self.name = name
        if competition not in self.competitions:
            self.competitions.append(competition)

    @property
    def data(self):
        """
        returns game dict
        """
        return self.__dict__
