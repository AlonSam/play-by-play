class SegevPlayerItem(object):
    """
    class for player data from Segev Sports
    """
    competitions = []

    def __init__(self, item, team_id):
        self.id = int(item['id'])
        self.team_id = int(team_id)
        self.name = item['firstName'].capitalize()
        for n in item['lastName'].split(' '):
            self.name += ' ' + n.capitalize()
        self.hebrew_name = item['firstNameLocal']
        for n in item['lastNameLocal'].split(' '):
            self.hebrew_name += ' ' + n.capitalize()
        self.shirt_number = item['jerseyNumber']

    @property
    def data(self):
        """
        returns game dict
        """
        return self.__dict__
