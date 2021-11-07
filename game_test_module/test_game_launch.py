import unittest
import time
import psutil
import pydirectinput
import pyautogui as pg
from multiprocessing import Process, Manager
from runGame import Game
from setting.game_config import GAME_WINDOWS_WIDTH, GAME_WINDOWS_HEIGHT, GAME_NAME


def launch_game(share_value):
    game = Game(GAME_WINDOWS_WIDTH, GAME_WINDOWS_HEIGHT, GAME_NAME)
    game.run_game(share_value)


class TestGameLaunch(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_game_options(self):
        with Manager() as manager:
            game_process = manager.dict()
            game_process["game_info"] = None
            game_process["game_top_score"] = None
            p = Process(target=launch_game, args=(game_process,))
            p.start()
            time.sleep(1)
            pg.moveTo(980, 540)
            # 游戏启动
            self.assertEqual(game_process["game_top_score"], True)
            # 按下start game
            pydirectinput.press("enter")
            time.sleep(1)
            self.assertEqual(game_process["game_info"], 1)
            self.assertEqual(game_process["game_top_score"], False)
            # 按下esc暂停游戏
            pydirectinput.press("escape")
            # 按下restart重新开始游戏
            pydirectinput.press("down")
            pydirectinput.press("enter")
            time.sleep(1)
            self.assertEqual(game_process["game_info"], 0)
            self.assertEqual(game_process["game_top_score"], True)
            # # 按下start game
            pydirectinput.press("enter")
            time.sleep(1)
            self.assertEqual(game_process["game_info"], 1)
            self.assertEqual(game_process["game_top_score"], False)
            # 按下esc 暂停游戏
            pydirectinput.press("escape")
            time.sleep(1)
            self.assertEqual(game_process["game_info"], 0)
            self.assertEqual(game_process["game_top_score"], True)
            # 按下continue 继续游戏
            pydirectinput.press("enter")
            self.assertEqual(game_process["game_info"], 1)
            self.assertEqual(game_process["game_top_score"], False)
            pg.moveTo(1910, 15)
            pg.click()
            time.sleep(1)

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
