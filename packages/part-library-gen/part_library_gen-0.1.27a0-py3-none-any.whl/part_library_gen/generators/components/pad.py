from decimal import Decimal


class Pad:
    def __init__(self, number: int, x: Decimal, y: Decimal, width: Decimal, height: Decimal):
        self.number = number
        self.x = x  # pad center
        self.y = y  # pad center
        self.width = width
        self.height = height

    def __str__(self):
        return f"Pad {self.number} ({self.x} {self.y} {self.width} {self.height})"

    def __repr__(self):
        return self.__str__()