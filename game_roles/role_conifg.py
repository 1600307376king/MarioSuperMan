#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/2/4 19:06
# @Author : jjc

# 图片放大倍数
SCALE_MULTIPLE = 3


def scale_tuple(tp, multiple):
    temp_tuple = [i * multiple for i in tp]
    return tuple(temp_tuple)


# 玩家角色状态, 每一种状态加载图片对应部分
player_img_path = 'resource/img/mario_bros.png'
player_img_load_dic = {
    'normal': {'img_path': player_img_path, 'position': scale_tuple((178, 32, 12, 16), SCALE_MULTIPLE)},
    'normal-2': {'img_path': player_img_path, 'position': scale_tuple((178, 24, 16, 20), SCALE_MULTIPLE)},
}

# 关卡类别
game_level_path = 'resource/img/level_1.png'
game_level_dic = {
    'level-1-1': {'img_path': game_level_path, 'position': (0, 0, 1920, 1080)}
}

# 文本配置
text_font_path = 'resource/font/Fixedsys500c.ttf'
text_size = 30

# 获取金币图片
coin_img_path = 'resource/img/text_images.png'
coin_img_load_dic = {
    'img_path': coin_img_path,
    'position': scale_tuple((90, 18, 8, 9), 5)
}

# 游戏开始界面logo
game_start_logo = 'resource/img/title_screen.png'
game_start_logo_dic = {
    'img_path': game_start_logo,
    'position': scale_tuple((0, 60, 178, 88), SCALE_MULTIPLE)
}

# 游戏选项指示
game_option_point = 'resource/img/title_screen.png'
game_option_point_dic = {
    'img_path': game_option_point,
    'position': scale_tuple((0, 153, 11, 11), SCALE_MULTIPLE)
}

