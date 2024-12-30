from e_simulator.geometry import Coordinate, Geometry, PolygonGeometry, CircleGeometry
from e_simulator.utils import Color
from .em_field import EMField, StaticEMField, VaryingEMField


# Electromagnetic region to declare the field in a specific region
class EMRegion:
    def __init__(self, em_field: EMField, geometry: Geometry, name: str|None = None, color: Color|None = None):
        self.name = name
        self.em_field = em_field
        self.geometry = geometry
        self.color = color

    @classmethod
    def from_dict(cls, data: dict|None):
        if not data: return None
        if not (data.get('em_field') and data.get('geometry')): raise ValueError('Invalid EMRegion data')
        em_field = StaticEMField.from_dict(data.get('em_field')) or VaryingEMField.from_dict(data.get('em_field'))
        geometry = PolygonGeometry.from_dict(data.get('geometry')) or CircleGeometry.from_dict(data.get('geometry'))
        return cls(
            em_field,
            geometry,
            data.get('name'),
            Color.from_hex(data.get('color'))
        )

    def apply(self, position: Coordinate):
        if self.geometry.check_in(position): return self.em_field
        return EMField()

    def __repr__(self):
        return f'EMRegion ({self.name or "Unknown"})'

    def to_dict(self):
        return {
            'name': self.name,
            'em_field': self.em_field.to_dict(),
            'geometry': self.geometry.to_dict(),
            'color': self.color.to_hex() if self.color else None
        }