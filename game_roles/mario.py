#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/2/4 19:18
# @Author : jjc
import pygame
from game_roles.role_conifg import player_img_load_dic, SCALE_MULTIPLE
from game_roles.base_element import BaseElement
from game_config import MAX_VERTICAL_VELOCITY, MAX_HORIZON_VELOCITY


class Mario(BaseElement):
    def __init__(self, x, y, img, obj_name=""):
        super().__init__(x, y, obj_name)
        self.image = img
        self.image = pygame.transform.scale(
            self.image, (self.image.get_rect().width * 3,
                         self.image.get_rect().height * 3))
        self.rect = self.image.get_rect()
        self.game_score = 0
        self.accelerated = pygame.Vector2(0, 0)
        self.initial_velocity = pygame.Vector2(0, 0)
        self.direction = pygame.Vector2(-1, 1)
        # self.vertical_accelerated = 0

    def run(self):
        pass

    def jump(self):
        # print(12)
        if self.initial_velocity.y == 0:
            # self.initial_velocity.y = -5
            # self.accelerated.y = 5
            self.initial_velocity.y = -10
            # self.initial_velocity.y += self.accelerated.y
            # if self.initial_velocity.y < 0:
            #     self.initial_velocity.y = max(self.initial_velocity.y, MAX_VERTICAL_VELOCITY)
            # self.update()

    def change_state(self):
        pass

    def fire(self):
        pass

    def init_accelerated(self):
        self.accelerated.x, _ = 0, 0

    def init_vertical_state(self):
        self.accelerated.y = 0
        self.initial_velocity.y = 0

    def decelerate(self):
        if self.initial_velocity.x > 0 and self.initial_velocity.y == 0:
            self.accelerated.x = 1
            self.initial_velocity.x += self.direction.x * self.accelerated.x
            # self.update()
        elif self.initial_velocity.x < 0 and self.initial_velocity.y == 0:
            self.accelerated.x = -1
            self.initial_velocity.x += self.direction.x * self.accelerated.x
            # self.update()
        if self.initial_velocity.y != 0:
            self.accelerated.y = 2
        self.initial_velocity.y += self.direction.y * self.accelerated.y

    def right_move(self):
        self.accelerated.x = 2
        self.initial_velocity += self.accelerated
        # self.initial_velocity.x = max(self.initial_velocity.x, MAX_HORIZON_VELOCITY)
        if self.initial_velocity.x >= 0:
            self.initial_velocity.x = min(self.initial_velocity.x, MAX_VERTICAL_VELOCITY)
        else:
            self.initial_velocity.x = max(self.initial_velocity.x, -MAX_VERTICAL_VELOCITY)
        # self.update()

    def left_move(self):
        self.accelerated.x = -2
        self.initial_velocity += 1 * self.accelerated
        if self.initial_velocity.x >= 0:
            self.initial_velocity.x = min(self.initial_velocity.x, MAX_VERTICAL_VELOCITY)
        else:
            self.initial_velocity.x = max(self.initial_velocity.x, -MAX_VERTICAL_VELOCITY)
        # self.update()

    def update(self):
        self.rect.x += self.initial_velocity.x
        self.rect.y += self.initial_velocity.y
