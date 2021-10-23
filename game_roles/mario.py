#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/2/4 19:18
# @Author : jjc
import pygame
from game_roles.role_conifg import player_img_load_dic, SCALE_MULTIPLE
from game_roles.base_element import BaseElement
from game_roles.state_mode import StateMode
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
        self.jump_initial_velocity = -20
        self.jump_gravity = 2
        self.accelerated_x = 6
        self.slow_down_decelerate = 4
        self.mario_state = StateMode()

    def keep_rise(self):
        self.accelerated.y = self.jump_gravity
        self.initial_velocity.y += self.direction.y * self.accelerated.y
        self.mario_state.vertical_state = "rise"
        # 减速后最小速度为0
        if self.initial_velocity.y >= 0:
            self.mario_state.vertical_state = "fall"

    def set_vertical_init_velocity(self):
        self.initial_velocity.y = self.jump_initial_velocity

    def keep_fall(self):
        self.accelerated.y = self.jump_gravity
        self.initial_velocity.y += self.direction.y * self.accelerated.y
        self.mario_state.vertical_state = "fall"

    def init_accelerated(self):
        self.accelerated.x, _ = 0, 0

    def init_vertical_state(self):
        self.accelerated.y = 0
        self.initial_velocity.y = 0
        self.mario_state.vertical_state = "vertical_static"

    def movement_horizon(self):
        if self.mario_state.vertical_state not in ("rise", "fall"):
            if self.mario_state.state == "right_move":
                self.right_move()

            elif self.mario_state.state == "left_move":
                self.left_move()

            elif self.mario_state.state == "right_decelerate":
                self.right_decelerate()

            elif self.mario_state.state == "left_decelerate":
                self.left_decelerate()

    def movement_vertical(self):
        if self.mario_state.vertical_state == "rise":
            self.keep_rise()
        elif self.mario_state.vertical_state == "fall":
            self.keep_fall()

    def right_decelerate(self):
        # 向右运动时减速
        if self.initial_velocity.x > 0 and self.initial_velocity.y == 0:
            self.accelerated.x = self.slow_down_decelerate
            self.initial_velocity.x += self.direction.x * self.accelerated.x
            self.mario_state.state = "right_decelerate"
            # 减速后最小速度为0
            if self.initial_velocity.x <= 0:
                self.initial_velocity.x = 0
                self.mario_state.state = "static"

    def left_decelerate(self):
        # 向左运动时减速

        if self.initial_velocity.x < 0 and self.initial_velocity.y == 0:
            self.accelerated.x = -self.slow_down_decelerate
            self.initial_velocity.x += self.direction.x * self.accelerated.x
            self.mario_state.state = "left_decelerate"
            # 减速后最小速度为0
            if self.initial_velocity.x >= 0:
                self.initial_velocity.x = 0
                self.mario_state.state = "static"

    def right_move(self):

        self.slow_down_decelerate = 1
        self.accelerated.x = self.accelerated_x
        self.initial_velocity += self.accelerated
        if self.initial_velocity.x >= 0:
            self.initial_velocity.x = min(self.initial_velocity.x, MAX_VERTICAL_VELOCITY)
        else:
            self.initial_velocity.x = max(self.initial_velocity.x, -MAX_VERTICAL_VELOCITY)
        self.mario_state.state = "right_move"

    def left_move(self):
        self.slow_down_decelerate = 1
        self.accelerated.x = -self.accelerated_x
        self.initial_velocity += self.accelerated
        if self.initial_velocity.x >= 0:
            self.initial_velocity.x = min(self.initial_velocity.x, MAX_VERTICAL_VELOCITY)
        else:
            self.initial_velocity.x = max(self.initial_velocity.x, -MAX_VERTICAL_VELOCITY)
        self.mario_state.state = "left_move"

    def towards_the_right(self):
        if "right_move" in self.mario_state.state_transform(self.mario_state.state):
            self.mario_state.state = "right_move"

    def towards_the_left(self):
        if "left_move" in self.mario_state.state_transform(self.mario_state.state):
            self.mario_state.state = "left_move"

    def towards_the_right_decelerate(self):
        if "right_decelerate" in self.mario_state.state_transform(self.mario_state.state):
            self.mario_state.state = "right_decelerate"

    def towards_the_left_decelerate(self):
        if "left_decelerate" in self.mario_state.state_transform(self.mario_state.state):
            self.mario_state.state = "left_decelerate"

    def towards_the_rise(self):
        if "rise" in self.mario_state.vertical_state_transform(self.mario_state.vertical_state):
            self.set_vertical_init_velocity()
            self.mario_state.vertical_state = "rise"

    def towards_the_fall(self):
        if "fall" in self.mario_state.vertical_state_transform(self.mario_state.vertical_state):
            self.mario_state.vertical_state = "fall"

    def update(self):
        self.rect.x += self.initial_velocity.x
        self.rect.y += self.initial_velocity.y

