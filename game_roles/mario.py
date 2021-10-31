#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/2/4 19:18
# @Author : jjc
import pygame
from game_roles.role_conifg import player_img_load_dic, SCALE_MULTIPLE
from game_roles.base_element import BaseElement
from game_roles.state_mode import StateMode
from game_config import MAX_VERTICAL_VELOCITY, MAX_HORIZON_VELOCITY, MARIO_INIT_POS_1
from game_roles.block_surface import BlockSurface


class Mario(BaseElement):
    def __init__(self, x, y, img, obj_name=""):
        super().__init__(x, y, obj_name)
        self.image = img
        self.image = pygame.transform.scale(
            self.image, (self.image.get_rect().width * 3,
                         self.image.get_rect().height * 3))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = MARIO_INIT_POS_1
        self.game_score = 0
        self.accelerated = pygame.Vector2(0, 0)
        # 马里奥运动瞬时运动
        self.instantaneous_velocity = pygame.Vector2(0, 0)
        self.direction = pygame.Vector2(-1, 1)
        self.jump_initial_velocity = -20
        self.jump_gravity = 2
        self.accelerated_x = 6
        self.slow_down_decelerate = 4
        self.mario_state = StateMode()
        self.ban_on_left = True
        self.ban_on_right = True
        self.left_surface = BlockSurface((0, 255, 0), 1, 50, self.rect.x, self.rect.y)
        self.right_surface = BlockSurface((0, 0, 255), 1, 50, self.rect.right, self.rect.y)
        self.bottom_surface = BlockSurface((255, 165, 0), 36, 1, self.rect.x, self.rect.bottom)

    def keep_rise(self):
        self.accelerated.y = self.jump_gravity
        self.instantaneous_velocity.y += self.direction.y * self.accelerated.y
        self.mario_state.vertical_state = "rise"
        # 减速后最小速度为0
        if self.instantaneous_velocity.y >= 0:
            self.mario_state.vertical_state = "fall"

    def set_vertical_init_velocity(self):
        self.instantaneous_velocity.y = self.jump_initial_velocity

    def set_vertical_velocity_to_zero(self):
        self.instantaneous_velocity.y = -self.instantaneous_velocity.y

    def keep_fall(self):
        self.accelerated.y = self.jump_gravity
        self.instantaneous_velocity.y += self.direction.y * self.accelerated.y
        self.mario_state.vertical_state = "fall"

    def init_accelerated(self):
        self.accelerated.x, _ = 0, 0

    def init_vertical_state(self):
        self.accelerated.y = 0
        self.instantaneous_velocity.y = 0
        self.mario_state.vertical_state = "vertical_static"

    def ban_on_the_left(self):
        self.instantaneous_velocity.x = 0
        self.mario_state.state = "static"

    def ban_on_the_right(self):
        self.instantaneous_velocity.x = 0
        self.mario_state.state = "static"

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
        if self.instantaneous_velocity.x > 0 and self.instantaneous_velocity.y == 0:
            self.accelerated.x = self.slow_down_decelerate
            self.instantaneous_velocity.x += self.direction.x * self.accelerated.x
            self.mario_state.state = "right_decelerate"
            # 减速后最小速度为0
            if self.instantaneous_velocity.x <= 0:
                self.instantaneous_velocity.x = 0
                self.mario_state.state = "static"

    def left_decelerate(self):
        # 向左运动时减速

        if self.instantaneous_velocity.x < 0 and self.instantaneous_velocity.y == 0:
            self.accelerated.x = -self.slow_down_decelerate
            self.instantaneous_velocity.x += self.direction.x * self.accelerated.x
            self.mario_state.state = "left_decelerate"
            # 减速后最小速度为0
            if self.instantaneous_velocity.x >= 0:
                self.instantaneous_velocity.x = 0
                self.mario_state.state = "static"

    def right_move(self):

        self.slow_down_decelerate = 1
        self.accelerated.x = self.accelerated_x
        self.instantaneous_velocity += self.accelerated
        if self.instantaneous_velocity.x >= 0:
            self.instantaneous_velocity.x = min(self.instantaneous_velocity.x, MAX_VERTICAL_VELOCITY)
        else:
            self.instantaneous_velocity.x = max(self.instantaneous_velocity.x, -MAX_VERTICAL_VELOCITY)
        self.mario_state.state = "right_move"

    def left_move(self):
        self.slow_down_decelerate = 1
        self.accelerated.x = -self.accelerated_x
        self.instantaneous_velocity += self.accelerated
        if self.instantaneous_velocity.x >= 0:
            self.instantaneous_velocity.x = min(self.instantaneous_velocity.x, MAX_VERTICAL_VELOCITY)
        else:
            self.instantaneous_velocity.x = max(self.instantaneous_velocity.x, -MAX_VERTICAL_VELOCITY)
        self.mario_state.state = "left_move"

    def towards_the_right(self):
        if "right_move" in self.mario_state.state_transform(self.mario_state.state):
            # 上升或者下落状态按左右键失效
            if "vertical_static" not in self.mario_state.vertical_state_transform(self.mario_state.vertical_state):
                self.mario_state.state = "right_move"

    def towards_the_left(self):
        if "left_move" in self.mario_state.state_transform(self.mario_state.state):
            if "vertical_static" not in self.mario_state.vertical_state_transform(self.mario_state.vertical_state):
                self.mario_state.state = "left_move"

    def try_to_speed_cut(self):
        if self.mario_state.vertical_state == "vertical_static":
            if self.mario_state.state == "left_move":
                self.towards_the_left_decelerate()
            elif self.mario_state.state == "right_move":
                self.towards_the_right_decelerate()

    def is_right_move(self):
        return self.mario_state.state == "right_move"

    def is_left_move(self):
        return self.mario_state.state == "left_move"

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
        # print(self.mario_state.vertical_state)
        if "fall" in self.mario_state.vertical_state_transform(self.mario_state.vertical_state):
            self.mario_state.vertical_state = "fall"

    def towards_the_vertical_static(self):
        if "vertical_static" in self.mario_state.vertical_state_transform(self.mario_state.vertical_state):
            self.mario_state.vertical_state = "vertical_static"

    def towards_the_static(self):
        self.mario_state.state = "static"

    def update(self, bearing_surface_collision, left_surface_collision, right_surface_collision):

        # print(self.instantaneous_velocity)
        for block in bearing_surface_collision:
            # 避免下降过头，超过支撑面
            if self.instantaneous_velocity.y >= block.rect.top - self.rect.bottom and \
                    block.rect.top >= self.rect.bottom:
                self.rect.y += block.rect.top - self.rect.bottom
                # 检测是否碰撞
                if self.is_y_axis_down_collide(bearing_surface_collision):
                    self.ban_on_left = False
                    self.towards_the_vertical_static()
                    break

                self.towards_the_fall()

        for block in left_surface_collision:
            # 避免mario向左移动发生碰撞时移动过头
            print(self.rect.left, block.rect.right, self.instantaneous_velocity.x)
            if self.instantaneous_velocity.x >= self.rect.left - block.rect.right and \
                    block.rect.right <= self.rect.left:
                if self.is_x_axis_down_collide(left_surface_collision):
                    self.towards_the_static()
                    break
            pass

        if self.mario_state.vertical_state == "vertical_static":
            self.instantaneous_velocity.y = 0
            self.accelerated.y = 0

        self.rect.x += self.instantaneous_velocity.x
        self.rect.y += self.instantaneous_velocity.y
        # self.left_surface.rect.x, self.left_surface.rect.y = self.rect.x, self.rect.y
        # self.right_surface.rect.x, self.right_surface.rect.y = self.rect.right, self.rect.y
        # self.bottom_surface.rect.x, self.bottom_surface.rect.y = self.rect.x, self.rect.bottom
