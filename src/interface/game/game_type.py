from enum import Enum, unique


@unique
class GameType(Enum):
    general = 0
    classics = 1
    action_adventure = 2
    console = 3
    rpg = 4
    strategy = 5
    survival = 6
