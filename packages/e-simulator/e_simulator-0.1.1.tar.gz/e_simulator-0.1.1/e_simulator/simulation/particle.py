import math
from e_simulator.geometry import Vector, Coordinate
from e_simulator.utils import Color
from .em_field import EMField

class Particle:
    def __init__(self,
        mass: float,
        charge: float,
        init_position: Coordinate,
        init_velocity: Vector = Vector(0, 0),
        drag_coefficient: float = 0,
        name: str | None = None,
        color: Color|None = None
    ):
        if mass <= 0: raise ValueError('Mass must be greater than 0')
        if drag_coefficient < 0: raise ValueError('Drag coefficient must be positive')

        self.name = name
        self.mass = mass
        self.charge = charge
        self.init_position = init_position
        self.init_velocity = init_velocity
        self.drag_coefficient = drag_coefficient
        self.color = color

    @classmethod
    def from_dict(cls, data: dict|None):
        if not data: return None
        # Charge can be 0
        if (data.get('charge') is None) or not (data.get('mass') and data.get('init_position')):
            raise ValueError('Invalid particle data')
        return cls(
            data.get('mass'),
            data.get('charge'),
            Coordinate.from_dict(data.get('init_position')),
            Vector.from_dict(data.get('init_velocity')) or Vector(0, 0),
            data.get('drag_coefficient') or 0,
            data.get('name'),
            Color.from_hex(data.get('color'))
        )

    def get_acceleration(self, velocity: Vector, em_field: EMField, time: float, light_speed: float|None = None):
        electric_force = self.charge * em_field.get_electric(time)
        magnetic_force = self.charge * Vector(-velocity.y, velocity.x) * em_field.get_magnetic(time)
        drag_force = - self.drag_coefficient * velocity.length() * velocity

        total_force = electric_force + magnetic_force + drag_force

        if not light_speed:
            return total_force / self.mass # Non-relativistic
        return total_force / self.mass * math.sqrt(1 - velocity.length_squared() / light_speed ** 2) # Relativistic

    def to_dict(self):
        return {
            'name': self.name,
            'mass': self.mass,
            'charge': self.charge,
            'init_position': self.init_position.to_dict(),
            'init_velocity': self.init_velocity.to_dict(),
            'drag_coefficient': self.drag_coefficient,
            'color': self.color.to_hex() if self.color else None
        }

    def __repr__(self):
        return f'Particle ({self.name or "Unknown"})'