from src.interface.mumjolandia.pod_template import PODTemplate


class Game(PODTemplate):
    def __init__(self, game_name, game_id):
        self.name = game_name
        self.game_id = game_id

    def __str__(self):
        return self.name + '[' + str(self.game_id) + ']'
