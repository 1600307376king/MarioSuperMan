#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/2/4 5:26
# @Author : jjc

"""
game main
"""

import os
from sys import exit
import pygame
from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_RIGHT, K_LEFT, KEYUP
from pygame.locals import K_SPACE
from pygame.locals import K_RETURN, K_ESCAPE
from game_roles.game_text import Text
from game_roles.game_level import Level, LogoImg
from game_roles.mario import Mario
from game_roles.block_surface import Block, BlockSurface
from setting.game_config import TEXT_FONT_PATH_1
from setting.game_config import GAME_LEVEL_BG_IMG_1, GAME_START_LOGO_IMG
from setting.game_config import WHITE_TEXT
from setting.game_config import TEXT_SIZE_60, GAME_OPTION_INTERVAL
from setting.game_config import GAME_LEVEL_REC_1, GAME_START_CENTER_LOGO_REC
from setting.game_config import COIN_IMG, COIN_IMG_REC, SCALE_MULTIPLE_3, SCALE_MULTIPLE_5
from setting.game_config import GAME_OPTION_ICON, GAME_MUSHROOM_LOGO_REC
from setting.game_config import GAME_WINDOWS_WIDTH, GAME_WINDOWS_HEIGHT, GAME_NAME
from setting.game_config import GAME_OPTION_BASE_X, GAME_OPTION_BASE_Y
from setting.game_config import GAME_LEVEL_TEXT_INIT_POS, MARIO_TITLE_INIT_POS
from setting.game_config import TIME_REMAINING_TITLE_INIT_POS, GAME_SCORE_TEXT_INIT_POS
from setting.game_config import GAME_COIN_TEXT_INIT_POS, GAME_LEVEL_NUM_INIT_POS
from setting.game_config import GAME_OPTION_TEXT_OBJECT_ARR_1, GAME_OPTION_TEXT_OBJECT_ARR_2
from setting.game_config import GAME_OPTION_TEXT_ARR_1, GAME_OPTION_TEXT_ARR_2
from setting.game_config import GAME_MUSHROOM_INIT_POS
from setting.game_config import MARIO_INIT_POS_1, MARIO_BASE_IMG
from setting.game_config import GAME_MUSIC_FILE_PATH_1
from game_roles.game_music import RoleMusic
from pygame.sprite import Sprite
from setting.game_config import MARIO_INIT_REC_1


def scale_tuple(tp, multiple):
    temp_tuple = [i * multiple for i in tp]
    return tuple(temp_tuple)


def rect_scale(rec, tp, multiple):
    # rec.x *= multiple
    # rec.y *= multiple
    # rec.w *= multiple
    # rec.h *= multiple
    rec.x, rec.y, rec.w, rec.h = [i * multiple for i in tp]
    return rec


class Game:
    def __init__(self, width, height, caption, fps=60):
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
        self.option_val = 1
        self.game_progress = 0
        # 游戏窗口顶部信息栏对象
        self.game_info_dict = {}
        # 游戏开始阶段文本对象
        self.game_start_text = {}
        self.game_start_img = {}
        self.game_option_index = GAME_OPTION_TEXT_OBJECT_ARR_1
        # display_info = pygame.display.Info()
        # print(display_info.current_w, )
        self.bg_logo_list = {}

        self.person = {}
        # 修改窗口初始位置
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (0, 30)
        # 设置窗口大小
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption(self.caption)
        self.bearing_surface_group = pygame.sprite.Group()
        self.left_surface_group = pygame.sprite.Group()
        self.right_surface_group = pygame.sprite.Group()
        self.top_surface_group = pygame.sprite.Group()
        self.display_back_group = pygame.sprite.Group()
        self.display_font_group = pygame.sprite.Group()
        self.joysticks = []
        self.joysticks1 = None
        self.game_mario = None
        self.bgm = None

    def mario_init(self):
        mario = Mario(
            *MARIO_INIT_POS_1,
            pygame.image.load(MARIO_BASE_IMG),
            obj_name="mario")
        # mario.image = pygame.transform.scale(
        #     mario.image, (mario.image.get_rect().width * SCALE_MULTIPLE_3,
        #                   mario.image.get_rect().height * SCALE_MULTIPLE_3))
        # mario.rect = mario.img_rect
        # mario.rect = mario.image.get_rect()
        # mario.rect = rect_scale(mario.rect, MARIO_INIT_REC_1, SCALE_MULTIPLE_3)

        self.person[mario.obj_name] = mario
        self.game_mario = self.person["mario"]
        # self.bearing_surface_group.add(block)
        # self.bearing_surface_group.add(mario)

    def draw_all_person(self):
        # Sprite.draw(self.screen)
        for person in self.person.values():

            self.screen.blit(person.image, (person.x, person.y), person.rect)

    def game_text_init(self):

        mouse_pos = Text(
            0, 0, WHITE_TEXT,
            text="x = {0}, y = {1}".format(*pygame.mouse.get_pos()), obj_name="mouse_pos")
        mario_text = Text(
            *MARIO_TITLE_INIT_POS, WHITE_TEXT,
            text="MARIO", text_size=TEXT_SIZE_60, obj_name="mario_text")
        level_text = Text(
            *GAME_LEVEL_TEXT_INIT_POS, WHITE_TEXT,
            text="WORLD", text_size=TEXT_SIZE_60, obj_name="level_text")
        time_remaining_text = Text(
            *TIME_REMAINING_TITLE_INIT_POS, WHITE_TEXT,
            text="TIME", text_size=TEXT_SIZE_60, obj_name="time_remaining_text")
        score_text = Text(
            *GAME_SCORE_TEXT_INIT_POS, WHITE_TEXT,
            text="0".center(6, '0'), text_size=TEXT_SIZE_60, obj_name="score_text")
        coin_text = Text(
            *GAME_COIN_TEXT_INIT_POS, WHITE_TEXT,
            text=" x" + "0".rjust(2, '0'), text_size=TEXT_SIZE_60, obj_name="coin_text")
        game_level_num = Text(
            *GAME_LEVEL_NUM_INIT_POS, WHITE_TEXT,
            text="0-1".center(6, " "), text_size=TEXT_SIZE_60, obj_name="game_level_num")

        game_top_score = Text(
            GAME_OPTION_BASE_X, GAME_WINDOWS_HEIGHT - 200, WHITE_TEXT,
            text='TOP - 000000'.center(20, ' '), text_size=TEXT_SIZE_60, obj_name="game_top_score")

        game_info_horizon = Text(100, GAME_WINDOWS_HEIGHT // 2, WHITE_TEXT,
                                 text="horizon static", text_size=TEXT_SIZE_60, obj_name="game_info_horizon")

        game_info_vertical = Text(100, GAME_WINDOWS_HEIGHT // 2 + 200, WHITE_TEXT,
                                  text="vertical static", text_size=TEXT_SIZE_60, obj_name="game_info_vertical")

        for i, game_option_obj_name in enumerate(GAME_OPTION_TEXT_OBJECT_ARR_1):
            self.game_start_text[game_option_obj_name] = Text(
                GAME_OPTION_BASE_X, GAME_OPTION_BASE_Y + GAME_OPTION_INTERVAL * i, WHITE_TEXT,
                text=GAME_OPTION_TEXT_ARR_1[i].center(20, ' '),
                text_size=TEXT_SIZE_60, obj_name=game_option_obj_name)

        self.game_info_dict[mouse_pos.obj_name] = mouse_pos
        self.game_info_dict[mario_text.obj_name] = mario_text
        self.game_info_dict[level_text.obj_name] = level_text
        self.game_info_dict[time_remaining_text.obj_name] = time_remaining_text
        self.game_info_dict[score_text.obj_name] = score_text
        self.game_info_dict[coin_text.obj_name] = coin_text
        self.game_info_dict[game_level_num.obj_name] = game_level_num
        self.game_info_dict[game_top_score.obj_name] = game_top_score
        # self.game_info_dict[game_info_horizon.obj_name] = game_info_horizon
        # self.game_info_dict[game_info_vertical.obj_name] = game_info_vertical

    def game_text_draw(self):
        for txt in self.game_info_dict.values():
            if txt.is_show:
                self.screen.blit(
                    pygame.font.Font(
                        TEXT_FONT_PATH_1, txt.text_size
                    ).render(txt.text, True, txt.text_color), (txt.x, txt.y))

        if self.game_progress == 0:
            for i, option_obj_name in enumerate(self.game_option_index):
                option_obj = self.game_start_text[option_obj_name]
                option_obj.y = GAME_OPTION_BASE_Y + GAME_OPTION_INTERVAL * i
                self.screen.blit(
                    pygame.font.Font(
                        TEXT_FONT_PATH_1, option_obj.text_size
                    ).render(option_obj.text, True, option_obj.text_color), (option_obj.x, option_obj.y))

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
            *GAME_MUSHROOM_INIT_POS, pygame.image.load(GAME_OPTION_ICON),
            scale_tuple(GAME_MUSHROOM_LOGO_REC, SCALE_MULTIPLE_3),
            obj_name="mushroom_icon")
        mushroom_icon.img.set_colorkey((255, 0, 220))
        mushroom_icon.img = pygame.transform.scale(mushroom_icon.img, (mushroom_icon.img.get_width() * SCALE_MULTIPLE_3,
                                                                       mushroom_icon.img.get_height() * SCALE_MULTIPLE_3))

        self.bg_logo_list[level.obj_name] = level
        self.bg_logo_list[game_coin_logo.obj_name] = game_coin_logo

        self.game_start_img[game_start_center_logo.obj_name] = game_start_center_logo
        self.game_start_img[mushroom_icon.obj_name] = mushroom_icon

    def game_bg_logo_draw(self):
        for img_obj in self.bg_logo_list.values():
            if img_obj.is_show:
                self.screen.blit(img_obj.img, (img_obj.x, img_obj.y), img_obj.img_rect)

        if self.game_progress == 0:
            for img_obj in self.game_start_img.values():
                if img_obj.is_show:
                    self.screen.blit(img_obj.img, (img_obj.x, img_obj.y), img_obj.img_rect)

    def mushroom_icon_move(self, direction):
        if self.game_progress == 0:
            if self.option_val == 1:
                self.game_start_img["mushroom_icon"].y += max(0, direction) * 80
                self.option_val += max(0, direction)
            elif 1 < self.option_val < len(self.game_option_index):
                self.game_start_img["mushroom_icon"].y += direction * 80
                self.option_val += direction
            elif self.option_val == len(self.game_option_index):
                self.game_start_img["mushroom_icon"].y += min(0, direction) * 80
                self.option_val += min(0, direction)

    def joystick_init(self):
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.joysticks1 = self.joysticks[0]

    def keyboard_control(self, event):
        if event.type == QUIT:
            exit()

        if event.type == KEYUP:
            self.game_mario.slow_down_decelerate = 4
            # print(self.game_mario.mario_state.state)
            self.game_mario.try_to_speed_cut()

        if event.type == KEYDOWN:

            if event.key == K_UP:
                self.mushroom_icon_move(-1)
            elif event.key == K_DOWN:
                self.mushroom_icon_move(1)
            elif event.key == K_RETURN:
                # 开始游戏
                if self.game_progress == 0 and \
                        self.game_option_index[self.option_val - 1] == "game_option_start":
                    self.game_progress = 1
                    self.option_val = 1
                    self.game_info_dict["game_top_score"].is_show = False

                # 游戏继续
                elif self.game_progress == 0 and \
                        self.game_option_index[self.option_val - 1] == "game_option_continue":
                    self.game_progress = 1
                    self.option_val = 1
                    self.game_info_dict["game_top_score"].is_show = False

                elif self.game_progress == 0 and \
                        self.game_option_index[self.option_val - 1] == "game_option_restart":
                    self.game_option_index = GAME_OPTION_TEXT_OBJECT_ARR_1
                    self.game_start_text.clear()
                    for i, game_option_obj_name in enumerate(GAME_OPTION_TEXT_OBJECT_ARR_1):
                        self.game_start_text[game_option_obj_name] = Text(
                            GAME_OPTION_BASE_X, GAME_OPTION_BASE_Y + GAME_OPTION_INTERVAL * i, WHITE_TEXT,
                            text=GAME_OPTION_TEXT_ARR_1[i].center(20, ' '), text_size=TEXT_SIZE_60,
                            obj_name=game_option_obj_name)

                    self.game_start_img["mushroom_icon"].y = GAME_MUSHROOM_INIT_POS[1]
                    self.game_progress = 0
                    self.option_val = 1
                    self.game_info_dict["game_top_score"].is_show = True

                # 选择exit选项时 退出游戏
                elif self.game_progress == 0 and \
                        self.game_option_index[self.option_val - 1] == "game_option_exit":
                    self.running = False

            elif event.key == K_ESCAPE:
                # 暂停游戏
                if self.game_progress == 1:
                    self.game_option_index = \
                        GAME_OPTION_TEXT_OBJECT_ARR_2

                    self.game_start_text.clear()
                    for i, game_option_obj_name in enumerate(GAME_OPTION_TEXT_OBJECT_ARR_2):
                        self.game_start_text[game_option_obj_name] = Text(
                            GAME_OPTION_BASE_X, GAME_OPTION_BASE_Y + GAME_OPTION_INTERVAL * i, WHITE_TEXT,
                            text=GAME_OPTION_TEXT_ARR_2[i].center(20, ' '), text_size=TEXT_SIZE_60,
                            obj_name=game_option_obj_name)
                    self.game_progress = 0
                    self.option_val = 1
                    self.game_info_dict["game_top_score"].is_show = True

            if self.game_progress == 1:
                if event.key == K_SPACE:
                    # mario jump
                    if self.game_mario.up_velocity == 0:
                        self.game_mario.towards_the_rise()

    def joystick_control(self, event):
        if event.type == pygame.JOYBUTTONUP or event.type == pygame.JOYBUTTONDOWN:
            buttons = self.joysticks1.get_numbuttons()
            for i in range(buttons):
                button = self.joysticks1.get_button(i)
                if i == 0 and button == 1:
                    print("press A")

                elif i == 1 and button == 1:
                    print("press B")

    def all_control(self):
        """
        所有操控函数集合
        :return:
        """
        for event in pygame.event.get():
            self.keyboard_control(event)

        if self.game_progress == 1:
            # 游戏开始时运行对mario的操作
            self.game_process_1_control()

    def block_state_auto_update(self):
        """
        游戏block对象状态自动更新，包括撞到建筑物后更新状态，碰撞检测等
        :return:
        """
        # 游戏进行时对mario的状态更新
        if self.game_progress == 1:
            # 根据当前状态保持水平方向运动或静止
            self.game_mario.movement_horizon()
            # 根据当前状态保持垂直方向的运动或静止
            self.game_mario.movement_vertical()

            self.game_mario.collision_check(self.bearing_surface_group, self.left_surface_group,
                                            self.right_surface_group)

    def game_process_1_control(self):
        """
        游戏进行时的键盘控制
        :return: None
        """
        keyboard_key = pygame.key.get_pressed()
        if not (keyboard_key[pygame.K_RIGHT] or keyboard_key[pygame.K_LEFT]):
            self.game_mario.try_to_speed_cut()

        if keyboard_key[pygame.K_RIGHT]:
            self.game_mario.towards_the_right()

        if keyboard_key[pygame.K_LEFT]:
            self.game_mario.towards_the_left()

    def all_block_position_update(self):
        """
        所以block的坐标更新
        :return:
        """
        if self.game_progress == 1:
            self.game_mario.update()

    def all_back_block_draw(self):
        if self.game_progress == 1:
            self.display_back_group.draw(self.screen)

    def all_font_block_draw(self):
        if self.game_progress == 1:
            self.display_font_group.draw(self.screen)

    def load_game_progress_1_music(self):
        self.bgm = RoleMusic(pygame.mixer.Sound(GAME_MUSIC_FILE_PATH_1))

    def play_music(self):
        # 游戏开始时播放背景音乐
        # 且只播放一次
        if not self.bgm.is_playing and self.game_progress == 1:
            self.bgm.music.play()
            self.bgm.is_playing = True
        if self.game_progress == 0 and self.bgm is not None:
            self.bgm.music.stop()
            self.bgm.is_playing = False

    def run_game(self, share_game_data=None):
        """
        launch game
        :param share_game_data: test module var
        :return:
        """
        self.running = True
        pygame.mixer.init()
        self.load_game_progress_1_music()
        self.mario_init()
        self.game_bg_logo_init()
        self.game_text_init()

        block2 = Block((0, 0, 255), 10, 1100, 0, 0)

        block3 = Block((255, 0, 255), 80, 93, 1348, 911)

        block4 = Block((0, 255, 255), 80, 140, 1829, 864)
        block5 = Block((0, 0, 255), 10, 1100, 1920, 0)

        ground = Block((0, 0, 255), 1920, 60, 0, 1005)
        ground.image.convert_alpha()

        self.bearing_surface_group.add(ground)
        self.bearing_surface_group.add(block3)
        self.bearing_surface_group.add(block4)

        self.left_surface_group.add(block3)
        self.left_surface_group.add(block4)
        self.left_surface_group.add(block2)
        self.left_surface_group.add(block5)

        self.right_surface_group.add(block3)
        self.right_surface_group.add(block4)
        self.right_surface_group.add(block2)
        self.right_surface_group.add(block5)

        self.display_font_group.add(self.game_mario)
        self.display_back_group.add(ground)
        self.display_back_group.add(block4)
        self.display_back_group.add(block3)
        self.display_back_group.add(block2)
        while self.running:
            # self.game_info_dict["game_info_horizon"].text = self.game_mario.mario_state.state
            # self.game_info_dict["game_info_vertical"].text = self.game_mario.mario_state.vertical_state
            self.block_state_auto_update()

            self.all_control()

            # 更新运动状态
            self.all_block_position_update()

            self.clock.tick(self.fps)

            self.all_back_block_draw()
            # 绘制游戏背景图片及logo
            self.game_bg_logo_draw()
            # 绘制游戏文本类
            self.game_text_draw()

            self.all_font_block_draw()

            self.play_music()
            self.game_info_dict["mouse_pos"].text = "x = {0}, y = {1}".format(*pygame.mouse.get_pos())
            if share_game_data:
                share_game_data["game_info"] = self.game_progress
                share_game_data["game_top_score"] = self.game_info_dict["game_top_score"].is_show

            pygame.display.update()


if __name__ == '__main__':
    game = Game(GAME_WINDOWS_WIDTH, GAME_WINDOWS_HEIGHT, GAME_NAME)

    # mario = Mario(150, 1005)
    game.run_game()
