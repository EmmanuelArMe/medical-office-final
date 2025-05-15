from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional
from typing import Dict, Any, ClassVar

    
class PacienteBase(BaseModel):
    nombre: str = Field(..., description="Nombre del paciente")
    apellido: str = Field(..., description="Apellido del paciente")
    fecha_nacimiento: date = Field(..., description="Fecha de nacimiento del paciente")
    documento: str = Field(..., description="Número de documento del paciente")
    telefono: str = Field(..., description="Número de teléfono del paciente")
    email: str = Field(..., description="Email del paciente")

    @field_validator("nombre", "apellido", "documento", "telefono", "email", mode="before", check_fields=True)
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value
    
    model_config: ClassVar[Dict[str, Any]] = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Juan",
                    "apellido": "Pérez",
                    "fecha_nacimiento": "1990-01-01",
                    "documento": "12345678",
                    "telefono": "123456789",
                    "email": "example@mail.com"
                }
            ]
        }
    }

class PacienteCreate(PacienteBase):
    pass

class PacienteResponse(PacienteBase):
    id: int
    nombre: str
    telefono: Optional[str] = None
    email: Optional[str] = None

class PacienteUpdate(PacienteBase):
    pass

    class Config:
        orm_mode = True
        from_attributes = True
