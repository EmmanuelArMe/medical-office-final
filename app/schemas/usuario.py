from pydantic import BaseModel, Field, field_validator
from typing import ClassVar, Dict, Any


class UsuarioBase(BaseModel):
    username: str = Field(..., description="Nombre de usuario")
    password: str = Field(..., description="Contraseña del usuario")
    rol_id: int = Field(..., description="ID del rol asociado al usuario")

    @field_validator("username", "password", "rol_id", mode="before")
    def validate_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value
    
    model_config: ClassVar[Dict[str, Any]] = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "jdoe",
                    "password": "secreta123",
                    "rol_id": 1
                }
            ]
        }
    }

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    id: int


    class Config:
        orm_mode = True

class UsuarioUpdate(UsuarioBase):
    
    class Config:
        orm_mode = True