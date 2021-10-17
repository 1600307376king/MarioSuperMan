#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/2/4 19:18
# @Author : jjc
import pygame
from game_roles.role_conifg import player_img_load_dic, SCALE_MULTIPLE
from game_roles.base_element import BaseElement


class Mario(BaseElement):
    def __init__(self, x, y, img, img_rect, obj_name=""):
        super().__init__(x, y, obj_name)
        self.image = img
        self.rect = self.image.get_rect()
        self.game_score = 0

    def run(self):
        pass

    def jump(self):
        pass

    def change_state(self):
        pass

    def fire(self):
        pass
