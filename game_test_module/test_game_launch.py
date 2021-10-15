import unittest
from runGame import Game
from game_config import GAME_WINDOWS_WIDTH, GAME_WINDOWS_HEIGHT, GAME_NAME
import time

game_copy = None


class TestGameLaunch(unittest.TestCase):

    def setUp(self):
        game = Game(GAME_WINDOWS_WIDTH, GAME_WINDOWS_HEIGHT, GAME_NAME)
        global game_copy
        game_copy = game
        game.run_game()

    def tearDown(self):
        pass

    def test_game_launch(self):
        time.sleep(3)
        game_copy.running = False

