import math
from e_simulator import PolygonGeometry, CircleGeometry, Coordinate, Geometry

class BoundsLimit:
    def __init__(self, geometry: Geometry):
        self.x_limit = ()
        self.y_limit = ()

        if isinstance(geometry, PolygonGeometry):
            self._set_polygon_lim(geometry)
        if isinstance(geometry, CircleGeometry):
            self._set_circle_lim(geometry)

    def __repr__(self):
        return f'BoundsLimit ({self.x_limit}, {self.y_limit})'

    def _set_polygon_lim(self, geometry: PolygonGeometry):
        x_list = [coordinate.x for coordinate in geometry.coordinates]
        y_list = [coordinate.y for coordinate in geometry.coordinates]
        self.x_limit = min(x_list) - 5, max(x_list) + 5
        self.y_limit = min(y_list) - 5, max(y_list) + 5

    def _set_circle_lim(self, geometry: CircleGeometry):
        base_angle_data = {
            0: geometry.center + Coordinate(geometry.radius, 0),
            1: geometry.center + Coordinate(0, geometry.radius),
            2: geometry.center + Coordinate(-geometry.radius, 0),
            3: geometry.center + Coordinate(0, -geometry.radius)
        }
        start_angle = geometry.start_angle
        end_angle = geometry.start_angle + geometry.central_angle
        considering_vertices = [
            geometry.center,
            geometry.center + Coordinate(geometry.radius * math.cos(start_angle), geometry.radius * math.sin(start_angle)),
            geometry.center + Coordinate(geometry.radius * math.cos(end_angle), geometry.radius * math.sin(end_angle))
        ]

        for i in range(4):
            if start_angle <= i * 0.5 * math.pi <= end_angle:
                considering_vertices.append(base_angle_data[i])

        x_list = [coordinate.x for coordinate in considering_vertices]
        y_list = [coordinate.y for coordinate in considering_vertices]
        self.x_limit = min(x_list) - 5, max(x_list) + 5
        self.y_limit = min(y_list) - 5, max(y_list) + 5