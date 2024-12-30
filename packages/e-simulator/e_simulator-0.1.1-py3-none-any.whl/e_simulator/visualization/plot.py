import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from e_simulator.utils import Color
from e_simulator.geometry import Geometry, PolygonGeometry, CircleGeometry, Coordinate


class PlotAxes:
    def __init__(self, axes: plt.Axes):
        self.axes = axes

    def __repr__(self):
        return f'PlotAxes ({self.axes})'

    def set_x_limit(self, limits: list[tuple[float, float]]):
        min_limits = [limit[0] for limit in limits]
        max_limits = [limit[1] for limit in limits]
        self.axes.set_xlim(max(min_limits), min(max_limits))

    def set_y_limit(self, limits: list[tuple[float, float]]):
        min_limits = [limit[0] for limit in limits]
        max_limits = [limit[1] for limit in limits]
        self.axes.set_ylim(max(min_limits), min(max_limits))

    def add_point(self, point: Coordinate, label: str, color: Color):
        return self.axes.plot(
            point.x,
            point.y,
            'o',
            color=color.to_hex(),
            label=label
        )[0]

    def add_orbit(self, orbit: list[Coordinate], label: str, color: Color, linewidth: float = 1):
        x_list = [point.x for point in orbit]
        y_list = [point.y for point in orbit]
        return self.axes.plot(
            x_list,
            y_list,
            color=color.to_normalized(),
            alpha=0.5,
            label=label,
            linewidth=linewidth
        )[0]

    def add_geometry(self, geometry: Geometry, color: Color|None = None, label: str|None = None, linewidth: float = 1):
        if isinstance(geometry, PolygonGeometry):
            return self._add_polygon(geometry, label, color, linewidth)
        if isinstance(geometry, CircleGeometry):
            return self._add_circle(geometry, label, color, linewidth)

    def _add_polygon(self, polygon: PolygonGeometry, label: str|None, color: Color|None, linewidth: float):
        polygon = patches.Polygon(
            [(coordinate.x, coordinate.y) for coordinate in polygon.coordinates],
            closed=True,
            facecolor=(color.to_normalized(), 0.4) if color else None,
            edgecolor=(color.to_normalized(), 1) if color else 'black',
            linewidth=linewidth,
            fill=color is not None,
            label=label
        )
        return self.axes.add_patch(polygon)

    def _add_circle(self, circle: CircleGeometry, label: str|None, color: Color|None, linewidth: float):
        start_theta = 180 * circle.start_angle / math.pi
        end_theta = 180 * (circle.start_angle + circle.central_angle) / math.pi
        circle = patches.Wedge(
            center=(circle.center.x, circle.center.y),
            r=circle.radius,
            theta1=start_theta,
            theta2=end_theta,
            facecolor=(color.to_normalized(), 0.4) if color else None,
            edgecolor=(color.to_normalized(), 1) if color else 'black',
            linewidth=linewidth,
            fill=color is not None,
            label=label
        )
        return self.axes.add_patch(circle)

