from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, ClassVar

class RolBase(BaseModel):
    id: int = Field(..., description="id del rol")
    nombre: str = Field(..., description="Nombre del rol")

    model_config: ClassVar[Dict[str, Any]] = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "nombre": "Administrador"
                }
            ]
        }
    }

    @field_validator("id","nombre", mode="before")
    def validate_nombre(cls, value):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError("El campo '{info.field_name}' es obligatorio.")
        return value

class RolCreate(RolBase):
    pass

class RolResponse(RolBase):
    id: int

class RolUpdate(RolBase):
    pass

    class Config:
        orm_mode = True