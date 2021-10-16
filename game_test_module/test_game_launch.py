import unittest
import time
import psutil
import threading
import pydirectinput
import pyautogui as pg
from multiprocessing import Process, Lock, Pool, Value, Manager
from runGame import Game
from game_config import GAME_WINDOWS_WIDTH, GAME_WINDOWS_HEIGHT, GAME_NAME


def launch_game(share_value):
    game = Game(GAME_WINDOWS_WIDTH, GAME_WINDOWS_HEIGHT, GAME_NAME)
    game.run_game(share_value)


class TestGameLaunch(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_start_game_button_state(self):
        with Manager() as manager:
            game_process = manager.dict()
            game_process["game_info"] = None
            p = Process(target=launch_game, args=(game_process,))
            p.start()
            time.sleep(1)
            pg.moveTo(980, 540)
            pydirectinput.press("enter")
            time.sleep(1)
            self.assertEqual(game_process["game_info"], 1)
            time.sleep(1)
            pg.moveTo(1910, 15)
            pg.click()
            time.sleep(1)
            if p.is_alive():
                p.close()

    def test_game_options_exit_quit(self):

        while True:
            time.sleep(2)
            pids = psutil.pids()
            python_exe_count = 0
            for pid in pids:
                ps = psutil.Process(pid)
                if "python3.exe" == ps.name():
                    python_exe_count += 1
            if python_exe_count <= 1:
                break

        p = Process(target=launch_game, args=(None,))
        p.start()

        self.assertEqual(p.is_alive(), True)
        time.sleep(2)
        pg.moveTo(980, 540)
        pg.click()
        pg.press("down")
        pg.press("down")
        # 使用pydirectinput 模块解决pyautogui 回车键无响应问题
        pydirectinput.press("enter")
        time.sleep(1)
        self.assertEqual(p.is_alive(), False)
