from enum import Enum
import math
from .vector import Coordinate


class GeometryType(Enum):
    POLYGON = 'polygon'
    CIRCLE = 'circle'

class Geometry:
    def __init__(self, geo_type: GeometryType):
        self.geo_type = geo_type

    def __repr__(self):
        return f'Geometry type <{self.geo_type}>'

    def check_in(self, point: Coordinate) -> bool:
        pass

    def to_dict(self) -> dict:
        pass

class PolygonGeometry(Geometry):
    def __init__(self, coordinates: list[Coordinate]):
        super().__init__(GeometryType.POLYGON)
        self.coordinates = coordinates

    @classmethod
    def simple_construct(cls, tuples: list[tuple[float, float]]):
        return cls([Coordinate(x, y) for x, y in tuples])

    @classmethod
    def from_dict(cls, data: dict|None):
        if not data: return None
        if not data.get('type') == GeometryType.POLYGON.value: return None
        if not data.get('coordinates'): raise ValueError('Invalid polygon data')
        return cls([Coordinate.from_dict(d) for d in data.get('coordinates')])

    def to_dict(self):
        return {
            'type': self.geo_type.value,
            'coordinates': [c.to_dict() for c in self.coordinates]
        }

    # Use Ray-Casting algorithm
    def check_in(self, point: Coordinate) -> bool:
        num_vertices = len(self.coordinates)
        crossings = 0
        for i in range(num_vertices):
            x1, y1 = self.coordinates[i].x, self.coordinates[i].y
            x2, y2 = self.coordinates[(i + 1) % num_vertices].x, self.coordinates[(i + 1) % num_vertices].y

            # The point exactly in the bound
            if (point.x - x1) * (point.y - y2) == (point.x - x2) * (point.y - y1):
                if min(y1, y2) <= point.y <= max(y1, y2) and min(x1, x2) <= point.x <= max(x1, x2):
                    return True

            if y1 == y2: continue
            if min(y1, y2) < point.y < max(y1, y2):
                x_intersect = (point.y - y1) * (x2 - x1) / (y2 - y1) + x1
                if point.x < x_intersect: crossings += 1
        return crossings % 2 == 1


class CircleGeometry(Geometry):
    def __init__(self,
        center: Coordinate,
        radius: float,
        start_angle: float = 0,
        central_angle: float = 2 * math.pi
    ):
        super().__init__(GeometryType.CIRCLE)
        self.center = center
        self.radius = radius
        if start_angle < 0 or start_angle > 2 * math.pi: raise ValueError('Angle out of range')
        self.start_angle = start_angle
        self.central_angle = central_angle if central_angle < 2 * math.pi else 2 * math.pi


    @classmethod
    def simple_construct(cls,
        center: tuple[float, float],
        radius: float,
        start_angle: float = 0,
        central_angle: float = 2 * math.pi
    ):
        return cls(Coordinate(*center), radius, start_angle, central_angle)

    @classmethod
    def from_dict(cls, data: dict|None):
        if not data: return None
        if not data.get('type') == GeometryType.CIRCLE.value: return None
        if not (data.get('center') and data.get('radius')): raise ValueError('Invalid circle data')
        return cls(
            Coordinate.from_dict(data.get('center')),
            data.get('radius'),
            data.get('start_angle', 0),
            data.get('central_angle', 2 * math.pi)
        )

    def to_dict(self):
        return {
            'type': self.geo_type.value,
            'center': self.center.to_dict(),
            'radius': self.radius,
            'start_angle': self.start_angle,
            'central_angle': self.central_angle
        }

    def check_in(self, point: Coordinate) -> bool:
        diff_vector = point - self.center
        if diff_vector.length() == 0: return True
        if diff_vector.length() > self.radius:
            return False

        if self.central_angle >= 2 * math.pi: return True
        angle = diff_vector.direction()

        if self.start_angle + self.central_angle < 2 * math.pi:
            return self.start_angle <= angle <= self.start_angle + self.central_angle
        else:
            return self.start_angle <= angle + 2 * math.pi <= self.start_angle + self.central_angle


