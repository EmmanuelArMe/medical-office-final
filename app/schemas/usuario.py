from pydantic import BaseModel, Field, field_validator
from typing import ClassVar, Dict, Any


class UsuarioBase(BaseModel):
    id: int = Field(..., description="ID del usuario")
    username: str = Field(..., description="Nombre de usuario")
    password: str = Field(..., description="Contraseña del usuario")
    rol_id: int = Field(..., description="ID del rol asociado al usuario")

    model_config: ClassVar[Dict[str, Any]] = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "username": "jdoe",
                    "password": "secreta123",
                    "rol_id": 1
                }
            ]
        }
    }

    @field_validator("id","username", "password", "rol_id", mode="before")
    def validate_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    id: int


    class Config:
        orm_mode = True

class UsuarioUpdate(UsuarioBase):
    
    class Config:
        orm_mode = True