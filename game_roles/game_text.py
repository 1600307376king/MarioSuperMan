#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/2/4 19:23
# @Author : jjc
import pygame
from game_roles.role_conifg import text_font_path, text_size, coin_img_load_dic, SCALE_MULTIPLE
from game_roles.role_conifg import game_start_logo_dic, game_option_point_dic


class Text(pygame.sprite.Sprite):

    def __init__(self, x, y, text='', text_font_size=text_size):
        super().__init__()
        pygame.font.init()
        self.x = x
        self.y = y
        self.position = self.x, self.y
        self.text = text
        self.text_font = pygame.font.Font(text_font_path, text_font_size)

    def get_role(self, screen):
        screen.blit(self.text_font.render(self.text, True, (255, 255, 255)), self.position)

    def change_position(self, x, y):
        self.x = x
        self.y = y
        self.position = x, y


class DynamicText(Text):
    def __init__(self, x, y, text='', text_font_size=text_size, text_type='none'):
        super().__init__(x, y, text, text_font_size=text_font_size)
        pygame.font.init()
        self.text_type = text_type

    # def get_role(self):
    #     return self.text_front.render(self.display_type[self.text_type], True, (255, 255, 255))
    def display_mouse_pos(self, screen):
        """
        显示当前鼠标坐标
        :return:
        """
        self.text = 'x = {0}, y = {1}'.format(*pygame.mouse.get_pos())
        screen.blit(self.text_font.render(self.text, True, (255, 255, 255)), self.position)

    def display_score(self, screen, score=0):
        """
        显示6位的分数
        例如 000123
        :param screen:
        :param score:
        :return:
        """
        self.text = str(score).rjust(6, '0')
        screen.blit(self.text_font.render(self.text, True, (255, 255, 255)), self.position)

    def display_coin_number(self, screen, coin_number=0):
        """
        显示金币数量
        :param screen:
        :param coin_number:
        :return:
        """
        self.text = 'x' + str(coin_number).rjust(2, '0')
        coin_rect = coin_img_load_dic['position']
        coin_img = pygame.image.load(coin_img_load_dic['img_path'])
        coin_img = pygame.transform.scale(coin_img, (coin_img.get_width() * 5, coin_img.get_height() * 5))
        coin_img.set_colorkey((0, 0, 0))
        coin_position = self.x - coin_rect[2], self.y + 10
        screen.blit(self.text_font.render(self.text, True, (255, 255, 255)), self.position)
        screen.blit(coin_img, coin_position, coin_rect)

    def display_level_number(self, screen, level_number=0):
        """
        显示关卡值
        :param screen:
        :param level_number:
        :return:
        """
        self.text = str(level_number) + '-1'
        screen.blit(self.text_font.render(self.text, True, (255, 255, 255)), self.position)

    def display_logo_img(self, screen):
        logo_rect = game_start_logo_dic['position']
        logo_img = pygame.image.load(game_start_logo_dic['img_path'])
        logo_img.set_colorkey((255, 0, 220))
        logo_img = pygame.transform.scale(logo_img, (logo_img.get_width() * SCALE_MULTIPLE, logo_img.get_height() * SCALE_MULTIPLE))
        logo_position = self.x, self.y
        screen.blit(logo_img, logo_position, logo_rect)

    def display_game_option(self, screen):
        # option_obj = self.text_font.render("Start Game".center(20, ' '), True, (255, 255, 255))
        # option_width, option_height = option_obj.get_rect()

        screen.blit(self.text_font.render("Start Game".center(20, ' '), True, (255, 255, 255)), self.position)

        screen.blit(self.text_font.render("Setting".center(20, ' '), True, (255, 255, 255)),
                    (self.position[0], self.position[1] + 80))

        screen.blit(self.text_font.render("Exit".center(20, ' '), True, (255, 255, 255)),
                    (self.position[0], self.position[1] + 160))

    def display_max_score(self, screen, score=0):
        """
        显示最高纪录
        :param score:
        :param screen:
        :return:
        """
        self.text = 'TOP - ' + str(score).rjust(6, '0')
        screen.blit(self.text_font.render(self.text, True, (255, 255, 255)), self.position)

    def display_option_point(self, screen):
        """
        游戏选项指示标记
        :param screen:
        :return:
        """
        point_rect = game_option_point_dic['position']
        point_img = pygame.image.load(game_option_point_dic['img_path'])
        point_img.set_colorkey((255, 0, 220))
        point_img = pygame.transform.scale(point_img, (point_img.get_width() * SCALE_MULTIPLE,
                                                       point_img.get_height() * SCALE_MULTIPLE))
        screen.blit(point_img, self.position, point_rect)


class StaticText(Text):
    pygame.font.init()

    # def display_text_group(self, screen, *group):
    #     for text_obj in group:
    #         screen.blit(text)


