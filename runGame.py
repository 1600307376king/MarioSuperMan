#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/2/4 5:26
# @Author : jjc

"""
game main
"""

import pygame
import math
from game_roles.game_level import Level, LogoImg
from game_roles.mario import Mario
from pygame.locals import QUIT, KEYUP, KEYDOWN, K_LEFT, K_UP, K_DOWN
from sys import exit
from settings import *
from game_roles.game_text import Text
from game_config import TEXT_SIZE_1
from game_config import TEXT_FONT_PATH_1
from game_config import GAME_LEVEL_BG_IMG_1, GAME_START_LOGO_IMG
from game_config import WHITE_TEXT, TEXT_SIZE_70, TEXT_SIZE_30, TEXT_SIZE_100
from game_config import TEXT_SIZE_60
from game_config import GAME_LEVEL_REC_1, GAME_START_CENTER_LOGO_REC
from game_config import COIN_IMG, COIN_IMG_REC, SCALE_MULTIPLE_3, SCALE_MULTIPLE_5
from game_config import GAME_OPTION_ICON, GAME_MUSHROOM_LOGO_REC


def scale_tuple(tp, multiple):
    temp_tuple = [i * multiple for i in tp]
    return tuple(temp_tuple)


class Game:
    def __init__(self, width, height, caption, fps=30):
        """

        :param width:游戏窗体宽度
        :param height: 高度
        :param caption: 窗体标题
        :param fps: 游戏帧率
        """
        pygame.init()

        self.width = width
        self.height = height
        self.caption = caption
        self.fps = fps
        self.running = False
        self.clock = pygame.time.Clock()
        self.counter = 0
        self.option_val = 1
        self.game_progress = 0
        self.text_display_list = {}
        self.bg_logo_list = {}
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption(self.caption)

    def game_text_init(self):

        mouse_pos = Text(
            0, 0, WHITE_TEXT, text="x = {0}, y = {1}".format(*pygame.mouse.get_pos()), obj_name="mouse_pos")
        mario_text = Text(
            100, 50, WHITE_TEXT, text="MARIO", text_size=TEXT_SIZE_60, obj_name="mario_text")
        level_text = Text(
            1300, 50, WHITE_TEXT, text="WORLD", text_size=TEXT_SIZE_60, obj_name="level_text")
        time_remaining_text = Text(
            1700, 50, WHITE_TEXT, text="TIME", text_size=TEXT_SIZE_60, obj_name="time_remaining_text")
        score_text = Text(
            100, 100, WHITE_TEXT, text="0".center(6, '0'), text_size=TEXT_SIZE_60, obj_name="score_text")
        coin_text = Text(
            800, 100, WHITE_TEXT, text=" x" + "0".rjust(2, '0'), text_size=TEXT_SIZE_60, obj_name="coin_text")
        game_level_num = Text(
            1300, 100, WHITE_TEXT, text="0-1".center(6, " "), text_size=TEXT_SIZE_60, obj_name="game_level_num")

        game_option_start = Text(
            630, 550, WHITE_TEXT,
            text="Start Game".center(20, ' '), text_size=TEXT_SIZE_60, obj_name="game_option_start")
        game_option_setting = Text(
            630, 550 + 80, WHITE_TEXT, "Setting".center(20, ' '),
            text_size=TEXT_SIZE_60, obj_name="game_option_setting")
        game_option_exit = Text(
            630, 550 + 160, WHITE_TEXT, "Exit".center(20, ' '),
            text_size=TEXT_SIZE_60, obj_name="game_option_exit")
        game_top_score = Text(
            730, 800, WHITE_TEXT,
            text='TOP - ' + "0".rjust(6, '0'), text_size=TEXT_SIZE_70, obj_name="game_top_score")

        self.text_display_list[mouse_pos.obj_name] = mouse_pos
        self.text_display_list[mario_text.obj_name] = mario_text
        self.text_display_list[level_text.obj_name] = level_text
        self.text_display_list[time_remaining_text.obj_name] = time_remaining_text
        self.text_display_list[score_text.obj_name] = score_text
        self.text_display_list[coin_text.obj_name] = coin_text
        self.text_display_list[game_level_num.obj_name] = game_level_num
        self.text_display_list[game_option_start.obj_name] = game_option_start
        self.text_display_list[game_option_setting.obj_name] = game_option_setting
        self.text_display_list[game_option_exit.obj_name] = game_option_exit
        self.text_display_list[game_top_score.obj_name] = game_top_score

    def game_text_draw(self):
        for txt in self.text_display_list.values():

            if txt.is_show:
                self.screen.blit(
                    pygame.font.Font(
                        TEXT_FONT_PATH_1, txt.text_size
                    ).render(txt.text, True, txt.text_color), (txt.x, txt.y))

    def game_bg_logo_init(self):
        # 初始化游戏背景
        level = Level(
            0, 0, pygame.image.load(GAME_LEVEL_BG_IMG_1), GAME_LEVEL_REC_1, obj_name="level")
        # 初始化游戏开始logo
        game_start_center_logo = LogoImg(
            700, 250, pygame.image.load(GAME_START_LOGO_IMG), scale_tuple(GAME_START_CENTER_LOGO_REC, SCALE_MULTIPLE_3),
            obj_name="game_start_center_logo")
        game_start_center_logo.img.set_colorkey((255, 0, 220))
        game_start_center_logo.img = \
            pygame.transform.scale(
                game_start_center_logo.img, (game_start_center_logo.img.get_width() * SCALE_MULTIPLE_3,
                                             game_start_center_logo.img.get_height() * SCALE_MULTIPLE_3))

        # 初始化顶部金币logo
        game_coin_logo = LogoImg(
            800, 100, pygame.image.load(COIN_IMG), scale_tuple(COIN_IMG_REC, SCALE_MULTIPLE_5),
            obj_name="game_coin_logo")
        game_coin_logo.img.set_colorkey((0, 0, 0))
        game_coin_logo.img = pygame.transform.scale(
            game_coin_logo.img,
            (game_coin_logo.img.get_width() * SCALE_MULTIPLE_5,
             game_coin_logo.img.get_height() * SCALE_MULTIPLE_5))
        game_coin_logo.x, game_coin_logo.y = game_coin_logo.x - COIN_IMG_REC[2], game_coin_logo.y + 10

        # 蘑菇头icon
        mushroom_icon = LogoImg(
            730, 565, pygame.image.load(GAME_OPTION_ICON), scale_tuple(GAME_MUSHROOM_LOGO_REC, SCALE_MULTIPLE_3),
            obj_name="mushroom_icon")
        mushroom_icon.img.set_colorkey((255, 0, 220))
        mushroom_icon.img = pygame.transform.scale(mushroom_icon.img, (mushroom_icon.img.get_width() * SCALE_MULTIPLE_3,
                                                   mushroom_icon.img.get_height() * SCALE_MULTIPLE_3))

        self.bg_logo_list[level.obj_name] = level
        self.bg_logo_list[game_start_center_logo.obj_name] = game_start_center_logo
        self.bg_logo_list[game_coin_logo.obj_name] = game_coin_logo
        self.bg_logo_list[mushroom_icon.obj_name] = mushroom_icon

    def game_bg_logo_draw(self):
        for img_obj in self.bg_logo_list.values():
            if img_obj.is_show:
                self.screen.blit(img_obj.img, (img_obj.x, img_obj.y), img_obj.img_rect)

    def mushroom_icon_move(self, direction):
        if self.game_progress == 0:
            if self.option_val == 1:
                self.bg_logo_list["mushroom_icon"].y += max(0, direction) * 80
                self.option_val += max(0, direction)
            elif self.option_val == 2:
                self.bg_logo_list["mushroom_icon"].y += direction * 80
                self.option_val += direction
            elif self.option_val == 3:
                self.bg_logo_list["mushroom_icon"].y += min(0, direction) * 80
                self.option_val += min(0, direction)

    def run_game(self):
        # pygame.joystick.init()
        # joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        # joysticks1 = joysticks[0]

        self.running = True
        self.game_bg_logo_init()
        self.game_text_init()

        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.mushroom_icon_move(-1)
                    elif event.key == K_DOWN:
                        self.mushroom_icon_move(1)
                # elif event.type == pygame.JOYBUTTONUP or event.type == pygame.JOYBUTTONDOWN:

                # buttons = joysticks1.get_numbuttons()
                #
                # for i in range(buttons):
                #     button = joysticks1.get_button(i)
                #     # print("i = {0}, button = {1}".format(i, button))
                #     if i == 0 and button == 1:
                #         print("press A")
                #         continue
                #
                #     elif i == 1 and button == 1:
                #         print("press B")
                #         continue

                # elif i == 5 and button == 1:
                #     print("press right")
                #
                # elif i == 5 and button == 1:
                #     print("press right")

                # elif event.type == pygame.JOYHATMOTION:
                #     # print(joysticks1.get_name())
                #     hat_buttons = joysticks1.get_numhats()
                #     for i in range(hat_buttons):
                #
                #         hat = joysticks1.get_hat(i)
                #         # print("i = {0}, ax = {1}".format(i, hat))
                #         if hat == (0, 1) and self.option_val > 1:
                #             print("上")
                #             self.option_val -= 1
                #             kwargs['game_option_point'].change_position(
                #                 kwargs['game_option_point'].x, kwargs['game_option_point'].y - 80)
                #             # print(kwargs['game_option_point'].position)
                #         elif hat == (1, 0):
                #             print("右")
                #         elif hat == (-1, 0):
                #             print("左")
                #         elif hat == (0, -1) and self.option_val < 3:
                #             print("下")
                #             self.option_val += 1
                #             kwargs['game_option_point'].change_position(
                #                 kwargs['game_option_point'].x, kwargs['game_option_point'].y + 80)
                # print(kwargs['game_option_point'].position)

            # keyboard_key = pygame.key.get_pressed()
            # if keyboard_key[pygame.K_UP]:
            #
            #
            # elif keyboard_key[pygame.K_DOWN]:
            #     self.mushroom_icon_move(1)
            # keyboard_key = pygame.key.get_pressed()
            # if keyboard_key[pygame.K_UP] and self.option_val > 0:
            #     self.option_val -= 1
            #     print(self.option_val)
            # elif keyboard_key[pygame.K_DOWN] and self.option_val < 3:
            #     self.option_val += 1
            #     print(self.option_val)

            self.clock.tick(self.fps)

            # 绘制游戏背景图片及logo
            self.game_bg_logo_draw()
            # 绘制游戏文本类
            self.game_text_draw()

            # 游戏背景

            # 鼠标坐标

            # mario text

            # kwargs['level'].get_role(screen)
            # # 显示玩家
            # kwargs['player'].display_player(screen)
            # 显示鼠标坐标

            # kwargs['mouse_pos_text'].display_mouse_pos(screen)
            # # 显示得分、关卡、剩余时间标题
            # for text_obj in kwargs['static_text_group']:
            #     text_obj.get_role(screen)
            #
            # # 显示当前得分
            # kwargs['score_text'].display_score(screen)
            #
            # # 显示金币数量
            # kwargs['coin_text'].display_coin_number(screen)
            #
            # # 显示当前关卡值
            # kwargs['game_level_number_text'].display_level_number(screen)
            #
            # # 显示游戏logo
            # kwargs['game_logo_img'].display_logo_img(screen)
            #
            # # 显示游戏选项
            # kwargs['game_option'].display_game_option(screen)
            #
            # # 显示游戏最高得分
            # kwargs['game_top_score'].display_max_score(screen)
            #
            # # 显示游戏选项指示
            # kwargs['game_option_point'].display_option_point(screen)
            # for obj in game_obj:
            #     if hasattr(obj, 'img_rect'):
            #         screen.blit(obj.get_role(), obj.position, obj.img_rect)
            #     else:
            #         screen.blit(obj.get_role(), obj.position)

            pygame.display.update()
            self.counter += 1


if __name__ == '__main__':
    game = Game(GAME_WINDOWS_WIDTH, GAME_WINDOWS_HEIGHT, GAME_NAME)
    # level = Level(0, 0)
    # mario = Mario(150, 1005)
    # mouse_pos_text = DynamicText(0, 0, text_font_size=20)
    # score_title_text = StaticText(100, 50, 'MARIO', 70)
    # level_title_text = StaticText(1200, 50, 'WORLD', 70)
    # time_remaining_text = StaticText(1600, 50, 'TIME', 70)
    # score_text = DynamicText(100, 100, text_font_size=60)
    # coin_text = DynamicText(800, 100, text_font_size=60)
    # game_level_number_text = DynamicText(1250, 100, text_font_size=60)
    # game_logo_img = DynamicText(700, 250)
    # game_option = DynamicText(630, 550, text_font_size=60)
    # game_top_score = DynamicText(730, 800, text_font_size=70)
    # game_option_point = DynamicText(730, 565)
    # static_text_list = (score_title_text, level_title_text, time_remaining_text)
    # role_dic = {
    #     'level': level,
    #     'player': mario,
    #     'mouse_pos_text': mouse_pos_text,
    #     'score_text': score_text,
    #     'static_text_group': static_text_list,
    #     'coin_text': coin_text,
    #     'game_level_number_text': game_level_number_text,
    #     'game_logo_img': game_logo_img,
    #     'game_option': game_option,
    #     'game_top_score': game_top_score,
    #     'game_option_point': game_option_point
    # }
    game.run_game()
    # while True:
    #
    #
    #     screen.blit(background, (0, 0))
    #     screen.blit(start_button_bg, (0, 0))
    #
    #     # x, y = pygame.mouse.get_pos()
    #
    #     pygame.display.update()
