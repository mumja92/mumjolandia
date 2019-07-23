from src.interface.mumjolandia.pod_template import PODTemplate


class Game(PODTemplate):
    def __init__(self, text, game_type, description):
        self.name = text
        self.description = description
        self.gameType = game_type

    def __str__(self):
        return self.name + ' - ' + self.description
