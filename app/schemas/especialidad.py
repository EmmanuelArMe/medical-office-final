from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, ClassVar

class EspecialidadBase(BaseModel):
    nombre: str = Field(..., description="Nombre de la especialidad")

    @field_validator("nombre", mode="before", check_fields=True)
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value
    
    model_config: ClassVar[Dict[str, Any]] = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Cardiología"
                }
            ]
        }
    }

class EspecialidadCreate(EspecialidadBase):
    pass

class EspecialidadResponse(EspecialidadBase):
    id: int

class EspecialidadUpdate(EspecialidadBase):
    pass

    class Config:
        orm_mode = True
