import marshal
from enum import Enum
from types import FunctionType
from typing import Callable
from e_simulator.geometry import Vector

# Electromagnetic field to declare strength and direction of the field
class EMFieldType(Enum):
    STATIC = 'static'
    VARYING = 'varying'

class EMField:
    def __init__(self, field_type: EMFieldType = EMFieldType.STATIC):
        self.field_type = field_type
        pass

    def __repr__(self):
        return f'EMField type <{self.field_type}>'

    def to_dict(self) -> dict:
        return {
            'type': EMFieldType.STATIC.value,
            'electric': Vector(0,0).to_dict(),
            'magnetic': 0
        }

    def get_electric(self, time: float) -> Vector:
        return Vector(0, 0)

    def get_magnetic(self, time: float) -> float:
        return 0

    def __add__(self, other):
        field_type = EMFieldType.STATIC
        if (self.field_type == EMFieldType.VARYING) or (other.field_type == EMFieldType.VARYING):
            field_type = EMFieldType.VARYING

        if field_type == EMFieldType.STATIC:
            return StaticEMField(
                electric = self.get_electric(0) + other.get_electric(0),
                magnetic = self.get_magnetic(0) + other.get_magnetic(0)
            )

        def get_electric(time: float) -> Vector:
            return self.get_electric(time) + other.get_electric(time)

        def get_magnetic(time: float) -> float:
            return self.get_magnetic(time) + other.get_magnetic(time)

        return VaryingEMField(get_electric, get_magnetic)

class StaticEMField(EMField):
    def __init__(self,
        electric: Vector = Vector(0, 0),
        magnetic: float = 0, # (+) -> in, (-) -> out
    ):
        super().__init__(EMFieldType.STATIC)
        self.electric = electric
        self.magnetic = magnetic

    @classmethod
    def from_dict(cls, data: dict|None):
        if not data: return None
        if data.get('type') != EMFieldType.STATIC.value: return None

        return cls(
            Vector.from_dict(data.get('electric')) or Vector(0,0),
            data.get('magnetic', 0),
        )

    def to_dict(self):
        return {
            'type': EMFieldType.STATIC.value,
            'electric': self.electric.to_dict(),
            'magnetic': self.magnetic
        }

    def get_electric(self, time: float) -> Vector:
        return self.electric

    def get_magnetic(self, time: float) -> float:
        return self.magnetic

class VaryingEMField(EMField):
    def __init__(self,
        get_electric: Callable[[float], Vector] = lambda t: Vector(0,0),
        get_magnetic: Callable[[float], float]  = lambda t: 0 # (+) -> in, (-) -> out
    ):
        super().__init__(EMFieldType.VARYING)
        self.get_electric = get_electric
        self.get_magnetic = get_magnetic

    @classmethod
    def from_dict(cls, data: dict | None):
        if not data: return None
        if data.get('type') != EMFieldType.VARYING.value: return None

        get_electric_code = marshal.loads(data.get('get_electric'))
        get_magnetic_code = marshal.loads(data.get('get_magnetic'))

        return cls(
            FunctionType(get_electric_code, globals(), closure=()),
            FunctionType(get_magnetic_code, globals(), closure=())
        )

    def to_dict(self):
        return {
            'type': EMFieldType.VARYING.value,
            'get_electric': marshal.dumps(self.get_electric.__code__),
            'get_magnetic': marshal.dumps(self.get_magnetic.__code__),
        }