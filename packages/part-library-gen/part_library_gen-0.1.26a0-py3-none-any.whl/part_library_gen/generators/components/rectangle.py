class Rectangle:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def to_dict(self):
        return {
            'width': self.width,
            'height': self.height,
            'x': self.x,
            'y': self.y
        }
