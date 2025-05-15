from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from typing import Dict, Any, ClassVar

class MedicoBase(BaseModel):
    nombre: str = Field(..., description="Nombre del médico")
    apellido: str = Field(..., description="Apellido del médico")
    especialidad_id: int = Field(..., description="ID de la especialidad del médico")
    email: Optional[EmailStr] = Field(None, description="Email del médico")
    telefono: Optional[str] = Field(None, description="Teléfono del médico")
    documento: str = Field(None, description="Número de documento del médico")

    @field_validator("documento", "nombre", "apellido", "especialidad_id", mode="before", check_fields=True)
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
                    "especialidad_id": 1,
                    "email": "example@mail.com",
                    "telefono": "123456789",
                    "documento": "12345678"
                }
            ]
        }
    }

class MedicoCreate(MedicoBase):
    pass

class MedicoResponse(MedicoBase):
    id: int

class MedicoUpdate(MedicoBase):
    pass
    class Config:
        from_attributes = True
