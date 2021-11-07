import pygame
import sys
from game_config import GAME_MUSIC_FILE_PATH_1


class RoleMusic:
    def __init__(self, music):
        self.music = music
        self.is_playing = False
