class Circle:
    def __init__(self, center_x, center_y, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

    def to_dict(self):
        return {
            'center_x': self.center_x,
            'center_y': self.center_y,
            'radius': self.radius
        }
