#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/2/4 19:22
# @Author : jjc
import pygame
import os
from game_roles.role_conifg import game_level_dic


class BaseImg:
    def __init__(self, x, y, img, img_rect):
        self.x = x
        self.y = y
        self.position = self.x, self.y
        self.img_rect = img_rect
        self.img = img


class Level(BaseImg):
    """
    游戏关卡
    """
    def __init__(self, x, y, img, img_rect, level='level-1-1'):
        super().__init__(x, y, img, img_rect)
        self.x = x
        self.y = y
        self.position = self.x, self.y
        self.img_rect = img_rect
        self.img = img
        self.is_show = True


class LogoImg(BaseImg):
    pass
    # def move(self):
    #     pass
    #
    # def get_role(self, screen):
    #     screen.blit(self.img, self.position, self.img_rect)

