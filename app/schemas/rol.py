from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, ClassVar

class RolBase(BaseModel):
    nombre: str = Field(..., description="Nombre del rol")

    @field_validator("nombre", mode="before")
    def validate_nombre(cls, value):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError("El campo '{info.field_name}' es obligatorio.")
        return value
    
    model_config: ClassVar[Dict[str, Any]] = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Administrador"
                }
            ]
        }
    }

class RolCreate(RolBase):
    pass

class RolResponse(RolBase):
    id: int

class RolUpdate(RolBase):
    pass

    class Config:
        orm_mode = True