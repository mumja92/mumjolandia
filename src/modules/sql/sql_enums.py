from enum import Enum


class Platform(Enum):
    PS3= 1
    PC = 2


class Drm(Enum):
    STEAM = 1
    ORIGIN = 2
    UPLAY = 3
    GOG = 4
    OTHER = 5


class Tag(Enum):
    single_player = 1
    multi_player = 2
    rpg = 3
    fps = 4
    rts = 5
    sport = 6
