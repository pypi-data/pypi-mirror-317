class Pin:
    def __init__(self, name, number, function, description: str, x: int, y: int, length: int, rotation: int,
                 name_visible=True):
        self.name = name
        self.name_visible = name_visible
        self.number = number
        self.number_visible = True
        self.function = function
        self.description = description
        self.x = x
        self.y = y
        self.length = length
        self.rotation = rotation

    def to_dict(self):
        return {
            'name': self.name,
            'name_visible': self.name_visible,
            'number': self.number,
            'number_visible': self.number_visible,
            'function': self.function,
            'description': self.description,
            'x': self.x,
            'y': self.y,
            'length': self.length,
            'rotation': self.rotation
        }

    def from_dict(self, data):
        self.name = data['name']
        self.name_visible = data['name_visible']
        self.number = data['number']
        self.number_visible = data['number_visible']
        self.function = data['function']
        self.description = data['description']
        self.x = data['x']
        self.y = data['y']
        self.length = data['length']
        self.rotation = data['rotation']
