import joblib
import pandas as pd
from typing import Callable
from e_simulator.geometry import *
from e_simulator.utils import Color
from .em_region import EMRegion
from .particle import Particle
from .simulator import Simulator, SimulateDataItem

class Project:
    def __init__(self,
        name: str|None = None,
        bg_color: Color|None = None
    ):
        self.name = name
        self.bg_color = bg_color
        self.bounds: Geometry|None = None
        self.particle: Particle|None = None
        self.em_regions: list[EMRegion] = []
        self.simulate_data: list[SimulateDataItem]|None = None

    def set_bounds(self, bounds: Geometry):
        self.bounds = bounds

    def set_particle(self, particle: Particle):
        self.particle = particle

    def set_em_regions(self, em_regions: list[EMRegion]):
        self.em_regions = em_regions

    def simulate(
        self,
        max_s: float | None = None,
        max_t: float | None = None,
        start_relativistic_ratio: float = 0.05, # Start relativistic simulation when velocity is greater than this ratio of light speed
        delta_t_func: Callable[[float], float] = lambda v: 1 / (v * 1e2), # Function to calculate delta_t based on velocity
        save_per_distance: float | None = None,
    ):
        if self.bounds is None: raise ValueError('Bounds not set')
        if self.particle is None: raise ValueError('Particle not set')
        self.simulate_data = Simulator.simulate(
            self.bounds,
            self.particle,
            self.em_regions,
            max_s, max_t,
            start_relativistic_ratio,
            delta_t_func,
            save_per_distance
        )

    def simulate_data_to_df(self):
        if self.simulate_data is None: return None
        data_dict = {
            'Time': [data.time for data in self.simulate_data],
            'Distance': [data.distance for data in self.simulate_data],
            'Position x': [data.position.x for data in self.simulate_data],
            'Position y': [data.position.y for data in self.simulate_data],
            'Velocity x': [data.velocity.x for data in self.simulate_data],
            'Velocity y': [data.velocity.y for data in self.simulate_data],
            'Kinetic': [data.kinetic for data in self.simulate_data],
            'Kinetic (eV)': [data.kinetic_in_ev for data in self.simulate_data]
        }
        return pd.DataFrame(data_dict)

    def system_dict(self):
        return {
            'name': self.name,
            'bg_color': self.bg_color.to_hex() if self.bg_color else None,
            'bounds': self.bounds.to_dict(),
            'particle': self.particle.to_dict(),
            'em_regions': [r.to_dict() for r in self.em_regions],
        }

    def export_system_joblib(self, path):
        system_dict = self.system_dict()
        joblib.dump(system_dict, path)

    def import_system_joblib(self, path):
        data = joblib.load(path)
        if data.get('name'): self.name = data.get('name')
        if data.get('bg_color'): self.bg_color = Color.from_hex(data.get('bg_color'))
        if data.get('bounds'): self.bounds = PolygonGeometry.from_dict(data.get('bounds')) or CircleGeometry.from_dict(data.get('bounds'))
        if data.get('particle'): self.particle = Particle.from_dict(data.get('particle'))
        if data.get('em_regions'): self.em_regions = [EMRegion.from_dict(d) for d in data.get('em_regions')]

    def import_simulate_data_csv(self, path: str):
        df = pd.read_csv(path)
        self.simulate_data = [
            SimulateDataItem(
                row['Time'],
                row['Distance'],
                Coordinate(row['Position x'], row['Position y']),
                Vector(row['Velocity x'], row['Velocity y']),
                row['Kinetic']
            ) for _, row in df.iterrows()
        ]

    def __repr__(self):
        return f'ESProject ({self.name or "Unknown"})'