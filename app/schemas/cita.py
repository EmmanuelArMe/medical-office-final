from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Dict, Any, ClassVar

class CitaBase(BaseModel):
    fecha: datetime
    paciente_id: int = Field(..., description="ID del paciente")
    medico_id: int = Field(..., description="ID del médico")
    consultorio_id: int = Field(..., description="ID del consultorio")
    motivo: str = Field(..., description="Motivo de la cita")

    @field_validator("paciente_id", "medico_id", "consultorio_id", "motivo", mode="before", check_fields=True)
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value
    
    model_config: ClassVar[Dict[str, Any]] = {
        "json_schema_extra": {
            "examples": [
                {
                    "fecha": "2023-10-01T10:00:00",
                    "paciente_id": 1,
                    "medico_id": 2,
                    "consultorio_id": 3,
                    "motivo": "Consulta general"
                }
            ]
        }
    }

class CitaCreate(CitaBase):
    pass

class CitaResponse(CitaBase):
    id: int

class CitaUpdate(CitaBase):
    pass

    class Config:
        from_attributes = True