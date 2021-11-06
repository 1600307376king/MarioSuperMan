from pygame import sprite


class BlockVelocity(sprite.Sprite):
    """
    all block instantaneous velocity
    """
    def __init__(self, *groups):
        super().__init__(*groups)
        self._left_velocity = 0
        self._right_velocity = 0
        self._down_velocity = 0
        self._up_velocity = 0

    @property
    def left_velocity(self):
        return self._left_velocity

    @left_velocity.setter
    def left_velocity(self, l_vel):
        if l_vel >= 0:
            self._left_velocity = 0
        else:
            self._left_velocity = l_vel
        self._right_velocity = 0

    @property
    def right_velocity(self):
        return self._right_velocity

    @right_velocity.setter
    def right_velocity(self, r_vel):
        if r_vel <= 0:
            self._right_velocity = 0
        else:
            self._right_velocity = r_vel
        self._left_velocity = 0

    @property
    def down_velocity(self):
        return self._down_velocity

    @down_velocity.setter
    def down_velocity(self, d_vel):
        if d_vel <= 0:
            self._down_velocity = 0
        else:
            self._down_velocity = d_vel
            self._up_velocity = 0

    @property
    def up_velocity(self):
        return self._up_velocity

    @up_velocity.setter
    def up_velocity(self, u_vel):
        if u_vel > 0:
            self._up_velocity = 0
        else:
            self._up_velocity = u_vel
        self._down_velocity = 0


class BaseElement(BlockVelocity):
    def __init__(self, x, y, obj_name=""):
        super().__init__()
        self.x = x
        self.y = y
        self.is_show = True
        self.obj_name = obj_name

    def is_y_axis_down_collide(self, bearing_surface_collision_arr):
        is_collide = False
        for block in bearing_surface_collision_arr:
            if self.rect.bottom >= block.rect.top and self.rect.top <= block.rect.bottom and \
                    not (self.rect.left > block.rect.right or self.rect.right < block.rect.left):
                is_collide = True

        return is_collide

    def is_x_axis_left_collide(self, left_surface_collision_arr):
        is_collide = False
        for block in left_surface_collision_arr:
            if self.rect.left <= block.rect.right and self.rect.right >= block.rect.left and \
                    not (self.rect.bottom < block.rect.top or self.rect.top > block.rect.bottom):
                is_collide = True
            if self.rect.top == block.rect.bottom or self.rect.bottom == block.rect.top:
                is_collide = False
        return is_collide

    def is_x_axis_right_collide(self, right_surface_collision_arr):
        is_collide = False
        for block in right_surface_collision_arr:
            if self.rect.right >= block.rect.left and self.rect.left <= block.rect.right and \
                    not (self.rect.bottom < block.rect.top or self.rect.top > block.rect.bottom):
                is_collide = True
            if self.rect.top == block.rect.bottom or self.rect.bottom == block.rect.top:
                is_collide = False
        return is_collide
