#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/2/4 19:23
# @Author : jjc

from game_roles.base_element import BaseElement


class Text(BaseElement):

    def __init__(self, x, y, txt_color, text='', text_size=30, obj_name=""):
        super().__init__(x, y, obj_name)
        self.text = text
        self.text_color = txt_color
        self.text_size = text_size

    def update_pos(self, x, y):
        self.x = x
        self.y = y
