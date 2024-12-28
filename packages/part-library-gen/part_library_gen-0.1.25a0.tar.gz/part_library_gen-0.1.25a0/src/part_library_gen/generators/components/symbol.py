class Part:
    def __init__(self, part_number, designator):
        self.part_number = part_number
        self.designator = designator
        self.pins = []
        self.body = []
        self.width = 0
        self.height = 0

    def add_pin(self, pin):
        self.pins.append(pin)

    def add_body(self, element):
        self.body.append(element)

    def to_dict(self):
        return {
            'part_number': self.part_number.to_dict(),
            'designator': self.designator.to_dict(),
            'pins': [x.to_dict() for x in self.pins],
            'body': [x.to_dict() for x in self.body],
            'width': self.width,
            'height': self.height
        }

    def form_dict(self, data):
        self.part_number.from_dict(data['part_number'])
        self.designator.from_dict(data['designator'])
        self.width = data['width']
        self.height = data['height']


class Symbol:
    def __init__(self, part_number: str, designator: str):
        self.part_number = part_number
        self.designator = designator
        self.parts = []

    def add_part(self, part):
        self.parts.append(part)

    def to_dict(self):
        return {
            'part_number': self.part_number,
            'designator': self.designator,
            'parts': [x.to_dict() for x in self.parts]
        }

    def form_dict(self, data):
        self.part_number = data['part_number']
        self.designator = data['designator']
