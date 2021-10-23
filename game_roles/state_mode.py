class StateMode:
    def __init__(self):
        self.state = "static"
        self.vertical_state = "vertical_static"
        self._state_map = {
            "static": ("right_move", "left_move"),
            "right_move": ("right_decelerate", ),
            "right_decelerate": ("right_move", "static"),
            "left_move": ("left_decelerate", ),
            "left_decelerate": ("left_move", "static")
        }

        self._vertical_state_map = {
            "rise": ("fall", ),
            "fall": ("vertical_static", ),
            "vertical_static": ("fall", "rise")
        }

    def state_transform(self, cur_state):
        return self._state_map[cur_state]

    def vertical_state_transform(self, vertical_state):
        return self._vertical_state_map[vertical_state]
