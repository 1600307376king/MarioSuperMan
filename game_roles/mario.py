#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/2/4 19:18
# @Author : jjc
import pygame
from game_roles.role_conifg import player_img_load_dic, SCALE_MULTIPLE


class Mario(object):
    def __init__(self, x, y, state='normal'):
        self.x = x
        self.y = y

        self.img_rect = player_img_load_dic[state]['position']
        _, _, self.width, self.height = self.img_rect
        self.img = pygame.image.load(player_img_load_dic[state]['img_path'])
        self.img = pygame.transform.scale(self.img, (self.img.get_rect().width * SCALE_MULTIPLE,
                                                     self.img.get_rect().height * SCALE_MULTIPLE))
        self.position = self.x + self.width / 2, self.y - self.height
        self.game_score = 0

    def get_role(self):

        return self.img

    def display_player(self, screen):
        screen.blit(self.img, self.position, self.img_rect)
        # return self.img

    def run(self):
        pass

    def jump(self):
        pass

    def change_state(self):
        pass

    def fire(self):
        pass
