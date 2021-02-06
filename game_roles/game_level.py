#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/2/4 19:22
# @Author : jjc
import pygame
import os
from game_roles.role_conifg import game_level_dic


class Level(object):
    """
    游戏关卡
    """
    def __init__(self, x, y, level='level-1-1'):
        self.x = x
        self.y = y
        self.position = self.x, self.y
        self.img_rect = game_level_dic[level]['position']
        self.img = pygame.image.load(game_level_dic[level]['img_path'])



    def move(self):
        pass

    def get_role(self, screen):
        screen.blit(self.img, self.position, self.img_rect)

