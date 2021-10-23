# 游戏窗口变量
GAME_WINDOWS_WIDTH = 1920
GAME_WINDOWS_HEIGHT = 1080
GAME_NAME = 'Mario Super Man'

# 游戏界面文字
MARIO_TEXT = "MARIO"
ZERO_TEXT = "0"
WORLD_TEXT = "WORLD"
TIME_TEXT = "TIME"
START_GAME_TEXT = "Start Game"
SETTING_TEXT = "Setting"
EXIT_TEXT = "Exit"
GAME_OPTION_INTERVAL = 80
GAME_OPTION_BASE_X = GAME_WINDOWS_WIDTH // 3
GAME_OPTION_BASE_Y = GAME_WINDOWS_HEIGHT // 2

# 放大倍数
SCALE_MULTIPLE_3 = 3
SCALE_MULTIPLE_5 = 5

# 文本配置
TEXT_FONT_PATH_1 = 'resource/font/Fixedsys500c.ttf'
TEXT_SIZE_1 = 30

# 游戏关卡图片
GAME_LEVEL_BG_IMG_1 = 'resource/img/level_1.png'
GAME_LEVEL_REC_1 = (0, 0, 1920, 1080)
GAME_LEVEL_TEXT_INIT_POS = (1300, 50)
# 关卡等级标签初始位置
GAME_LEVEL_NUM_INIT_POS = (1300, 100)

# 游戏开始界面logo
GAME_START_LOGO_IMG = 'resource/img/title_screen.png'
GAME_START_CENTER_LOGO_REC = (0, 60, 178, 88)

# 游戏顶部金币图片
COIN_IMG = 'resource/img/text_images.png'
COIN_IMG_REC = (90, 18, 8, 9)
# 获取金币数量标签初始位置
GAME_COIN_TEXT_INIT_POS = (800, 100)

# 选项蘑菇头icon
GAME_OPTION_ICON = 'resource/img/title_screen.png'
GAME_MUSHROOM_LOGO_REC = (0, 153, 11, 11)
GAME_MUSHROOM_INIT_POS = (730, GAME_OPTION_BASE_Y + 10)

# mario
MARIO_BASE_IMG = "resource/img/mario_bros_1.png"
MARIO_INIT_REC_1 = (178, 32, 12, 16)
MARIO_INIT_REC_2 = (178, 24, 16, 20)
MARIO_INIT_POS_1 = (600, 958)
MAX_HORIZON_VELOCITY = 5
MAX_VERTICAL_VELOCITY = 20

# 字体颜色
WHITE_TEXT = (255, 255, 255)

# 字体大小
TEXT_SIZE_70 = 70
TEXT_SIZE_30 = 30
TEXT_SIZE_60 = 60
TEXT_SIZE_100 = 100

# 马里奥标签初始位置
MARIO_TITLE_INIT_POS = (100, 50)

# 计时标签初始位置
TIME_REMAINING_TITLE_INIT_POS = (1700, 50)

# 游戏得分数值初始位置
GAME_SCORE_TEXT_INIT_POS = (100, 100)

GAME_OPTION_TEXT_OBJECT_ARR_1 = ("game_option_start", "game_option_setting", "game_option_exit")
GAME_OPTION_TEXT_ARR_1 = ("Start Game", "Setting", "Exit")

GAME_OPTION_TEXT_OBJECT_ARR_2 = \
    ("game_option_continue", "game_option_restart", "game_option_setting", "game_option_exit")
GAME_OPTION_TEXT_ARR_2 = \
    ("Continue", "Restart", "Setting", "Exit")

GAME_OPTION_TEXT_OBJECT_ARR_3 = \
    ("game_option_continue", "game_option_restart", "game_option_start", "game_option_setting", "game_option_exit")
GAME_OPTION_TEXT_ARR_3 = \
    ("Continue", "Restart", "Start Game", "Setting", "Exit")



