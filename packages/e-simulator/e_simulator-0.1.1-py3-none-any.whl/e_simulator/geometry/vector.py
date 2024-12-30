import math

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @classmethod
    def from_dict(cls, data: dict|None):
        if not data: return None
        if (data.get('x') is None) or (data.get('y') is None): raise ValueError('Invalid 2d data')
        return cls(data.get('x'), data.get('y'))

    def __repr__(self):
        return f'Vector ({self.x}, {self.y})'

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float|int):
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, other: float|int):
        return self.__mul__(other)

    def __truediv__(self, scalar: float|int):
        return Vector(self.x / scalar, self.y / scalar)

    def length_squared(self):
        return self.x ** 2 + self.y ** 2

    def length(self):
        return math.sqrt(self.length_squared())

    def direction(self):
        positive = self.y >= 0
        acos = math.acos(self.x / self.length())
        return acos if positive else 2 * math.pi - acos

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y
        }

class Coordinate(Vector):
    def __repr__(self):
        return f'Coordinate ({self.x}, {self.y})'
