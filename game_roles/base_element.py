from pygame import sprite


class BaseElement(sprite.Sprite):
    def __init__(self, x, y, obj_name="", *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.is_show = True
        self.obj_name = obj_name

    def is_y_axis_down_collide(self, bearing_surface_collision_arr):
        is_collide = False
        for block in bearing_surface_collision_arr:
            if self.rect.bottom >= block.rect.top and self.rect.top <= block.rect.bottom and \
                    not (self.rect.left > block.rect.right or self.rect.right < block.rect.left):
                # print(block.rect, self.rect)
                is_collide = True

        return is_collide

    def is_x_axis_down_collide(self, left_surface_collision_arr):
        is_collide = False
        for block in left_surface_collision_arr:
            if self.rect.left <= block.rect.right and self.rect.right >= block.rect.left and \
                    not (self.rect.bottom < block.rect.top or self.rect.top > block.rect.bottom):
                is_collide = True
        print(is_collide)
        return is_collide
