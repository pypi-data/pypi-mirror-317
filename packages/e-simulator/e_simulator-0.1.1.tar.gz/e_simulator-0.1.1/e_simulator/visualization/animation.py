import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from e_simulator.simulation import Project, SimulateDataItem

class Animation:
    def __init__(self, project: Project, plot_bounds_limit, plot_regions, plot_particle, plot_orbit, **kwargs):
        self.project = project
        self.plot_bounds_limit = plot_bounds_limit
        self.plot_regions = plot_regions
        self.plot_particle = plot_particle
        self.plot_orbit = plot_orbit
        self.kwargs = kwargs
        self.dpi = kwargs['image_width'] * 40

    def __repr__(self):
        return f'Animation ({self.project})'

    def export_gif(
        self,
        path: str,
    ):
        image_data_list = self._get_simulation_image_data_list()
        height_width_ratio = image_data_list[0].shape[0] / image_data_list[0].shape[1]
        frames = len(image_data_list)

        figure = plt.figure()
        axes = plt.axes()

        # remove padding
        figure.set_dpi(self.dpi)
        figure.set_size_inches(self.kwargs['image_width'], self.kwargs['image_width'] * height_width_ratio)
        figure.tight_layout(pad=0)
        figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

        axes.set_axis_off()
        im = axes.imshow(image_data_list[0], animated=True)
        def update(i: int):
            im.set_array(image_data_list[i])
            return im,

        # Create the animation object
        animation_figure = FuncAnimation(figure, update, frames=frames, interval=1/self.kwargs['fps'], cache_frame_data=False, blit=True, repeat_delay=500)
        animation_figure.save(path, writer='pillow', fps=self.kwargs['fps'])
        plt.close(figure)

    def _get_legend_data(self):
        figure, axes = plt.subplots()
        plot_geometry_list = self.plot_regions(axes)
        plot_particle = self.plot_particle(axes)
        plot_orbit =  self.plot_orbit(axes)
        legend_handles = [plot_orbit, plot_particle] + plot_geometry_list
        plt.close()

        image_width = self.kwargs['image_width']
        legend_cols = self.kwargs['legend_cols']
        legend_rows = len(legend_handles)//legend_cols + (1 if len(legend_handles) % legend_cols else 0)

        figure, axes = plt.subplots()
        axes.set_axis_off()
        axes.legend(handles=legend_handles, loc='center', ncol=self.kwargs['legend_cols'])

        figure.set_size_inches(image_width*(0.2 + 0.3*legend_cols), image_width*(1 + 0.5*legend_rows))
        figure.set_dpi(self.dpi)
        cache_dict = {'padding': [0.1, 0.3, 0.25, 0.25]}
        image_array = self._plt_to_array(figure, cache_dict)
        plt.close(figure)
        return image_array

    def _merge_legend_data(self, image_data, legend_data):
        legend_width = legend_data.shape[1]
        image_width = image_data.shape[1]

        data_to_add_cols = legend_data if legend_width <= image_width else image_data
        pad_width = abs(legend_width-image_width)
        data_to_add_cols = np.pad(
            data_to_add_cols,
            ((0, 0), (pad_width//2 + pad_width%2, pad_width//2), (0, 0)),
            mode='constant',
            constant_values=255)

        return np.concatenate(
            (image_data, data_to_add_cols) if legend_width <= image_width else (data_to_add_cols, legend_data),
            axis=0
        )

    def _get_simulation_image_data_list(self):
        image_data_list = []
        time = 0
        time_step = 1/(self.kwargs['fps'] * self.kwargs['slower_times'])


        cache_dict = {'legend_data': self._get_legend_data()} # cache data between frames
        for item in self.project.simulate_data:
            if item.time >= time:
                image_data_list.append(self._get_simulation_image_step(item, cache_dict))
                time += time_step
        return image_data_list

    def _get_simulation_image_step(self, data: SimulateDataItem, cache_dict):
        figure, axes = plt.subplots()
        figure.set_size_inches(5, 5)

        self.plot_bounds_limit(axes, self.kwargs['bounds_width'], self.kwargs['x_limit'], self.kwargs['y_limit'], self.kwargs['aspect_ratio'])
        self.plot_regions(axes, self.kwargs['region_width'])
        self.plot_orbit(axes, self.kwargs['orbit_width'])
        self.plot_particle(axes, data.position)

        # set text of data item
        axes.set_xlabel(
            f'Time: {data.time:.2f} s \nVelocity: {data.velocity.length():.3e} m/s \nKinetic: {data.kinetic:.3e} J ~ {data.kinetic_in_ev:.3e} eV',
            loc='left',
            labelpad=10,
            fontsize=8
        )

        axes.set_title(self.kwargs['title'].format(self.project.name) if self.kwargs['title'] else f'{self.project.name} simulation')

        figure.set_dpi(self.dpi)
        image_array = self._plt_to_array(figure, cache_dict)
        plt.close(figure)
        return image_array

    def _remove_white_space_array(self, image_array, cache_dict):
        if not cache_dict.get('white_space_left'):
            start_col = -1
            for col_i in range(image_array.shape[1]):
                if np.any(image_array[:, col_i, :3] < 200):  # White color
                    if start_col == -1: start_col = col_i
                    break
            cache_dict['white_space_left'] = start_col
        if not cache_dict.get('white_space_right'):
            start_col = -1
            for col_i in range(image_array.shape[1]):
                if np.any(image_array[:, -col_i, :3] < 200):  # White color
                    if start_col == -1: start_col = col_i
                    break
            cache_dict['white_space_right'] = start_col
        if not cache_dict.get('white_space_top'):
            start_row = -1
            for row_i in range(image_array.shape[0]):
                if np.any(image_array[row_i, :, :3] < 200):  # White color
                    if start_row == -1: start_row = row_i
                    break
            cache_dict['white_space_top'] = start_row
        if not cache_dict.get('white_space_bottom'):
            start_row = -1
            for row_i in range(image_array.shape[0]):
                if np.any(image_array[-row_i, :, :3] < 200):  # White color
                    if start_row == -1: start_row = row_i
                    break
            cache_dict['white_space_bottom'] = start_row

        dpi = self.dpi
        padding = cache_dict.get('padding') if cache_dict.get('padding') else [0.25, 0.2, 0.15, 0.25]
        left_start = cache_dict['white_space_left'] - int(padding[2]*dpi)
        if left_start > 0: image_array = image_array[:, left_start:, :]
        right_start = cache_dict['white_space_right'] - int(padding[3]*dpi)
        if right_start > 0: image_array = image_array[:, :-left_start, :]
        top_start = cache_dict['white_space_top'] - int(padding[0]*dpi)
        if top_start > 0: image_array = image_array[top_start:, :, :]
        bottom_start = cache_dict['white_space_bottom'] - int(padding[1]*dpi)
        if bottom_start > 0: image_array = image_array[:-bottom_start, :, :]
        return image_array

    def _plt_to_array(self, figure, cache_dict):
        figure.tight_layout(w_pad=0)
        figure.canvas.draw()
        image_array = np.array(figure.canvas.renderer.buffer_rgba())

        image_array = self._remove_white_space_array(image_array, cache_dict)
        if cache_dict.get('legend_data') is not None:
            image_array = self._merge_legend_data(image_array, cache_dict['legend_data'])
        return image_array
