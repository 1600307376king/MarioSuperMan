from pygame import sprite


class BaseElement(sprite.Sprite):
    def __init__(self, x, y, obj_name="", *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.is_show = True
        self.obj_name = obj_name
