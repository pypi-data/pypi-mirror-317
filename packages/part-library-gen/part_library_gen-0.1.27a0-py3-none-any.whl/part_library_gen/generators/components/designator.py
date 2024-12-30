class Designator:
    def __init__(self, designator, x, y):
        self.designator = designator
        self.x = x
        self.y = y

    def to_dict(self):
        return {
            'designator': self.designator,
            'x': self.x,
            'y': self.y
        }

    def from_dict(self, designator_dict):
        self.designator = designator_dict['designator']
        self.x = designator_dict['x']
        self.y = designator_dict['y']
