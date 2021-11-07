#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/2/4 19:18
# @Author : jjc
import pygame
import time
from game_roles.role_conifg import player_img_load_dic, SCALE_MULTIPLE
from game_roles.base_element import BaseElement
from game_roles.state_mode import StateMode
from setting.game_config import MAX_VERTICAL_VELOCITY, MAX_HORIZON_VELOCITY, MARIO_INIT_POS_1, SCALE_MULTIPLE_3
from game_roles.block_surface import BlockSurface
from game_roles.game_music import RoleMusic
from setting.game_config import MARIO_SMALL_JUMP_SOUND_PATH


class Mario(BaseElement):
    def __init__(self, x, y, img, obj_name=""):
        super().__init__(x, y, obj_name)
        self.all_image = img
        self.all_image = pygame.transform.scale(
            self.all_image, (self.all_image.get_rect().width * SCALE_MULTIPLE_3,
                             self.all_image.get_rect().height * SCALE_MULTIPLE_3))
        self.flip_image = pygame.transform.flip(self.all_image, True, False)
        self.init_draw_rect = (96 * SCALE_MULTIPLE_3, 0, 16 * SCALE_MULTIPLE_3, 16 * SCALE_MULTIPLE_3)
        self.image = self.all_image.subsurface(self.init_draw_rect)
        self.frame = 0
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = MARIO_INIT_POS_1
        self.game_score = 0
        self.direction = pygame.Vector2(-1, 1)
        self.jump_initial_velocity = -32
        self.global_gravity = 4
        self.accelerated_x = 6
        self.slow_down_decelerate = 4
        self.mario_state = StateMode()
        self.rect_state_matrix = tuple((16 * SCALE_MULTIPLE_3 * i, 0, 16 * SCALE_MULTIPLE_3, 16 * SCALE_MULTIPLE_3) for i in range(14))
        self.is_turn_right = True
        self.animation_unit = 16 * SCALE_MULTIPLE_3
        self.jump_music = RoleMusic(pygame.mixer.Sound(MARIO_SMALL_JUMP_SOUND_PATH))

    def sound_play(self):
        if not self.jump_music.is_playing:
            self.jump_music.music.play()

    def keep_rise(self):

        self.up_velocity += self.global_gravity
        self.mario_state.vertical_state = "rise"
        # 减速后最小速度为0
        if self.up_velocity >= 0:
            self.mario_state.vertical_state = "fall"

    def to_reserve_up_velocity(self):
        self.up_velocity = -self.up_velocity

    def keep_fall(self):
        self.down_velocity += self.global_gravity
        self.mario_state.vertical_state = "fall"

    def init_vertical_state(self):
        self.down_velocity = 0
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
        if self.right_velocity > 0 and self.up_velocity == 0 and self.down_velocity == 0:
            self.right_velocity += -1 * self.slow_down_decelerate
            self.mario_state.state = "right_decelerate"
            # 减速后最小速度为0
            if self.right_velocity == 0:
                self.mario_state.state = "static"

    def left_decelerate(self):
        # 向左运动时减速

        if self.left_velocity < 0 and self.up_velocity == 0 and self.down_velocity == 0:
            self.left_velocity += self.slow_down_decelerate
            self.mario_state.state = "left_decelerate"
            # 减速后最小速度为0
            if self.left_velocity == 0:
                self.mario_state.state = "static"

    def right_move(self):
        """
        keep right move
        :return:
        """
        self.slow_down_decelerate = 1
        self.right_velocity += self.accelerated_x
        self.right_velocity = min(self.right_velocity, MAX_VERTICAL_VELOCITY)
        self.mario_state.state = "right_move"
        self.right_move_animation()

    def left_move(self):
        """
        keep left move
        :return:
        """
        self.slow_down_decelerate = 1
        self.left_velocity += -self.accelerated_x
        self.left_velocity = max(self.left_velocity, -MAX_VERTICAL_VELOCITY)
        self.mario_state.state = "left_move"
        self.left_move_animation()

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
            self.up_velocity = self.jump_initial_velocity
            self.mario_state.vertical_state = "rise"
            self.sound_play()

    def towards_the_fall(self):
        # print(self.mario_state.vertical_state)
        if "fall" in self.mario_state.vertical_state_transform(self.mario_state.vertical_state):
            self.mario_state.vertical_state = "fall"

    def towards_the_vertical_static(self):
        if "vertical_static" in self.mario_state.vertical_state_transform(self.mario_state.vertical_state):
            self.mario_state.vertical_state = "vertical_static"

    def towards_the_static(self):
        self.mario_state.state = "static"
        self.left_velocity = 0
        self.right_velocity = 0

    def is_towards_the_left(self):
        return self.mario_state.state in ("left_decelerate", "left_move")

    def is_towards_the_right(self):
        return self.mario_state.state in ("right_decelerate", "right_move")

    def collision_check(self, bearing_surface_collision, left_surface_collision, right_surface_collision):

        for block in bearing_surface_collision:
            # 避免下降过头，超过支撑面
            if self.down_velocity >= block.rect.top - self.rect.bottom and \
                    block.rect.top >= self.rect.bottom:
                self.rect.y += block.rect.top - self.rect.bottom
                # 检测是否碰撞
                if self.is_y_axis_down_collide(bearing_surface_collision):
                    # self.towards_the_vertical_static()
                    self.init_vertical_state()
                    break

                self.towards_the_fall()

        if self.is_towards_the_left():
            for block in left_surface_collision:
                # 避免mario向左移动发生碰撞时移动过头

                if abs(self.left_velocity) >= self.rect.left - block.rect.right and \
                        block.rect.right <= self.rect.left:
                    self.rect.x += -(self.rect.left - block.rect.right)
                    if self.is_x_axis_left_collide(left_surface_collision):
                        self.towards_the_static()
                        break

        if self.is_towards_the_right():
            for block in right_surface_collision:
                if self.right_velocity >= block.rect.left - self.rect.right and \
                        block.rect.left >= self.rect.right:
                    self.rect.x += block.rect.left - self.rect.right
                    if self.is_x_axis_right_collide(left_surface_collision):
                        self.towards_the_static()
                        break

    def right_move_animation(self):
        self.init_draw_rect = self.rect_state_matrix[self.frame % 2]
        self.image = self.all_image.subsurface(self.init_draw_rect)
        self.is_turn_right = True

    def left_move_animation(self):
        self.init_draw_rect = self.rect_state_matrix[-1 * (self.frame % 2) - 1]
        self.image = self.flip_image.subsurface(self.init_draw_rect)
        self.is_turn_right = False

    def static_animation(self):
        if self.is_turn_right:
            self.init_draw_rect = (96 * SCALE_MULTIPLE_3, 0, 16 * SCALE_MULTIPLE_3, 16 * SCALE_MULTIPLE_3)
            self.image = self.all_image.subsurface(self.init_draw_rect)
        else:

            self.init_draw_rect = (96 * SCALE_MULTIPLE_3 + self.animation_unit, 0, 16 * SCALE_MULTIPLE_3, 16 * SCALE_MULTIPLE_3)
            self.image = self.flip_image.subsurface(self.init_draw_rect)

    # def left_decelerate_animation(self):
    #     self.init_draw_rect = self.rect_state_matrix[-4]
    #     self.image = self.flip_image.subsurface(self.init_draw_rect)
    #
    # def right_decelerate_animation(self):
    #     self.init_draw_rect = self.rect_state_matrix[3]
    #     self.image = self.all_image.subsurface(self.init_draw_rect)

    def jump_turn_right_animation(self):
        self.init_draw_rect = self.rect_state_matrix[4]
        self.image = self.all_image.subsurface(self.init_draw_rect)

    def jump_turn_left_animation(self):
        self.init_draw_rect = self.rect_state_matrix[-5]
        self.image = self.flip_image.subsurface(self.init_draw_rect)

    def check_static_to_change_animation(self):
        if self.mario_state.vertical_state == "vertical_static":
            if self.mario_state.state == "static":
                self.static_animation()
            elif self.mario_state.state == "right_move":
                self.right_move_animation()
            elif self.mario_state.state == "left_move":
                self.left_move_animation()
        elif self.mario_state.vertical_state == "rise":
            if self.is_turn_right:
                self.jump_turn_right_animation()
            elif not self.is_turn_right:
                self.jump_turn_left_animation()

            # elif self.mario_state.state == "right_decelerate":
            #     self.right_decelerate_animation()
            # elif self.mario_state.state == "left_decelerate":
            #     self.left_decelerate_animation()

        self.frame += 1

    def update(self):
        self.check_static_to_change_animation()
        self.rect.x += self.left_velocity + self.right_velocity
        self.rect.y += self.down_velocity + self.up_velocity
