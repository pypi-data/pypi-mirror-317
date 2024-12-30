class PartNumber:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y

    def to_dict(self):
        return {
            'text': self.text,
            'x': self.x,
            'y': self.y
        }

    def from_dict(self, part_number_dict):
        self.text = part_number_dict['text']
        self.x = part_number_dict['x']
        self.y = part_number_dict['y']
