import matplotlib.pyplot as plt
from e_simulator.geometry import Coordinate
from e_simulator.utils import Color
from e_simulator.simulation import Project
from e_simulator.visualization.animation import Animation
from e_simulator.visualization.bounds_limit import BoundsLimit
from e_simulator.visualization.plot import PlotAxes


class Visualizer:
    def __init__(self, project: Project):
        self.project = project
        self._cache_dict = {}

    def __repr__(self):
        return f'Visualizer ({self.project})'

    def plot_system(
        self,
        axes: plt.Axes,
        x_limit: tuple[float, float] | None = None,
        y_limit: tuple[float, float] | None = None,
        title: str | None = None,
        aspect_ratio: int = 1,
        legend_cols: int = 2,
        bounds_width: float = 2,
        region_width: float = 1,
    ):
        self.plot_bounds_limit(axes, bounds_width, x_limit, y_limit, aspect_ratio)
        plot_geometry_list = self.plot_regions(axes, region_width)
        plot_particle = self.plot_particle(axes, None)

        # set legend
        legend_handles = [plot_particle] + plot_geometry_list
        axes.legend(handles=legend_handles, loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=legend_cols)
        axes.set_title(title.format(self.project.name) if title else f'{self.project.name} system')

    def plot_simulation(
        self,
        axes: plt.Axes,
        x_limit: tuple[float, float] | None = None,
        y_limit: tuple[float, float] | None = None,
        title: str | None = None,
        aspect_ratio: int = 1,
        legend_cols: int = 2,
        bounds_width: float = 2,
        region_width: float = 1,
        orbit_width: float = 1
    ):
        self.plot_bounds_limit(axes, bounds_width, x_limit, y_limit, aspect_ratio)
        plot_geometry_list = self.plot_regions(axes, region_width)
        plot_orbit = self.plot_orbit(axes, orbit_width)

        # set legend
        legend_handles = [plot_orbit] + plot_geometry_list
        axes.legend(handles=legend_handles, loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=legend_cols)
        axes.set_title(title.format(self.project.name) if title else f'{self.project.name} simulation')

    def plot_orbit(self, axes: plt.Axes, linewidth: float = 1):
        if self.project.simulate_data is None: raise ValueError('Project has not been simulated')
        particle = self.project.particle
        simulate_data = self.project.simulate_data
        plot_axes = PlotAxes(axes)
        return plot_axes.add_orbit(
            [data.position for data in simulate_data],
            f'{particle.name or "Particle"} orbit',
            particle.color or Color(0, 0, 0),
            linewidth=linewidth,
        )

    def plot_bounds_limit(
        self,
        axes: plt.Axes,
        bounds_width: float = 2,
        x_limit: tuple[float, float] | None = None,
        y_limit: tuple[float, float] | None = None,
        aspect_ratio: int = 1
    ):
        if self.project.bounds is None: raise ValueError('Project bounds not set')
        bounds_limit = BoundsLimit(self.project.bounds)
        plot_axes = PlotAxes(axes)

        plot_axes.set_x_limit([bounds_limit.x_limit, x_limit] if x_limit else [bounds_limit.x_limit])
        plot_axes.set_y_limit([bounds_limit.y_limit, y_limit] if y_limit else [bounds_limit.y_limit])
        plot_axes.axes.set_aspect(aspect_ratio)

        plot_axes.add_geometry(self.project.bounds, self.project.bg_color, linewidth=bounds_width)

    def plot_regions(self, axes: plt.Axes, region_width: float = 1):
        plot_axes = PlotAxes(axes)
        plot_geometry_list = []
        for i in range(len(self.project.em_regions)):
            region = self.project.em_regions[i]
            plot_geometry = plot_axes.add_geometry(
                region.geometry,
                region.color,
                label=region.name or f'Region {i}',
                linewidth=region_width
            )
            plot_geometry_list.append(plot_geometry)
        return plot_geometry_list

    def plot_particle(self, axes: plt.Axes, coordinate: Coordinate|None = None):
        if self.project.particle is None: return
        particle = self.project.particle
        plot_axes = PlotAxes(axes)
        return plot_axes.add_point(
            coordinate or particle.init_position,
            particle.name or 'Particle',
            particle.color or Color(0, 0, 0)
        )

    def animation(
        self,
        slower_times: float = 1,
        fps: int = 10,
        x_limit: tuple[float, float] | None = None,
        y_limit: tuple[float, float] | None = None,
        title: str | None = None,
        aspect_ratio: int = 1,
        legend_cols: int = 2,
        bounds_width: float = 2,
        region_width: float = 1,
        orbit_width: float = 1,
        image_width: float = 5,
    ):
        return Animation(self.project, self.plot_bounds_limit, self.plot_regions, self.plot_particle, self.plot_orbit,
            slower_times=slower_times,
            fps=fps,
            x_limit=x_limit,
            y_limit=y_limit,
            title=title,
            legend_cols=legend_cols,
            bounds_width=bounds_width,
            region_width=region_width,
            orbit_width=orbit_width,
            image_width=image_width,
            aspect_ratio=aspect_ratio
        )