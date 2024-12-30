import math
import numpy as np
from typing import Callable
from e_simulator.geometry import Coordinate, Vector, Geometry
from .constants import Constants
from .em_field import EMField
from .particle import Particle
from .em_region import EMRegion

class SimulateDataItem:
    def __init__(self, time: float, distance: float, position: Coordinate, velocity: Vector, kinetic: float):
        self.time = time
        self.distance = distance
        self.position = position
        self.velocity = velocity
        self.kinetic = kinetic
        self.kinetic_in_ev = kinetic / Constants.elementary_charge

    def __repr__(self):
        return f'SimulateDataItem (t={self.time})'


class Simulator:
    @staticmethod
    def get_kinetic(particle: Particle, velocity: Vector, relativistic: bool = False):
        if not relativistic: return 0.5 * particle.mass * velocity.length_squared()
        gamma = math.sqrt(1 - velocity.length_squared() / Constants.light_speed ** 2)
        return particle.mass * Constants.light_speed ** 2 * (1/gamma - 1)

    @staticmethod
    def delta_runge_kutta(diff_func: Callable[[float, any], any], t_i: float, u_i: any, delta_t: float):
        k1 = diff_func(t_i, u_i)
        k2 = diff_func(t_i + delta_t / 2, u_i + delta_t * k1 / 2)
        k3 = diff_func(t_i + delta_t / 2, u_i + delta_t * k2 / 2)
        k4 = diff_func(t_i + delta_t, u_i + delta_t * k3)
        return (delta_t / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

    @staticmethod
    def get_new_data_item(
        old: SimulateDataItem,
        particle: Particle,
        em_field: EMField,
        delta_t_func: Callable[[float], float],
        relativistic: bool = False
    ):
        delta_t = delta_t_func(old.velocity.length())

        old_u = np.asarray([old.position.x, old.position.y, old.velocity.x, old.velocity.y])
        def diff_func(t: float, u):
            velocity = Vector(u[2], u[3])
            acceleration = particle.get_acceleration(velocity, em_field, t, Constants.light_speed if relativistic else None)
            return np.asarray([velocity.x, velocity.y, acceleration.x, acceleration.y])
        delta_u = Simulator.delta_runge_kutta(diff_func, old.time, old_u, delta_t)
        delta_position = Vector(delta_u[0], delta_u[1])
        delta_velocity = Vector(delta_u[2], delta_u[3])

        new_time = old.time + delta_t
        new_distance = old.distance + delta_position.length()
        new_position = old.position + delta_position
        new_velocity = old.velocity + delta_velocity
        new_kinetic = Simulator.get_kinetic(particle, new_velocity, relativistic)
        return SimulateDataItem(new_time, new_distance, new_position, new_velocity, new_kinetic)

    @staticmethod
    def simulate(
            bounds: Geometry,
            particle: Particle,
            em_regions: list[EMRegion],
            max_s: float | None,
            max_t: float | None,
            start_relativistic_ratio,
            delta_t_func: Callable[[float], float],
            save_per_distance: float | None,
    ):
        if not bounds.check_in(particle.init_position): raise ValueError('Particle initial position out of bounds')
        if save_per_distance and save_per_distance <= 0: raise ValueError('Save per distance should be greater than 0')
        data: list[SimulateDataItem] = [
            SimulateDataItem(0, 0, particle.init_position, particle.init_velocity,
                             Simulator.get_kinetic(particle, particle.init_velocity))
        ]

        last_data = data[0]
        num_saves = 1
        while True:
            if not bounds.check_in(last_data.position): break
            if max_s and last_data.distance >= max_s: break
            if max_t and last_data.time >= max_t: break

            relativistic = (last_data.velocity.length() / Constants.light_speed) > start_relativistic_ratio
            new_em_field = EMField()
            for em_region in em_regions:
                new_em_field += em_region.apply(last_data.position)

            last_data = Simulator.get_new_data_item(
                last_data,
                particle,
                new_em_field,
                delta_t_func,
                relativistic
            )
            if save_per_distance is None or last_data.distance/save_per_distance > num_saves:
                data.append(last_data)
                num_saves += 1

        return data