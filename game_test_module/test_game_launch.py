import unittest
import time
import pyautogui as pg
from runGame import Game
from game_config import GAME_WINDOWS_WIDTH, GAME_WINDOWS_HEIGHT, GAME_NAME


class TestGameLaunch(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_game_launch(self):
        x = 1910
        y = 15
        print(pg.position())
        pg.moveTo(x, y)
        time.sleep(2)
        pg.click()
        print(pg.position())

