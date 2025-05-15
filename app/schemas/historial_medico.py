from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import ClassVar, Dict, Any

class HistorialMedicoBase(BaseModel):
    descripcion: str = Field(..., description="Descripción del historial médico")
    fecha: datetime = Field(..., description="Fecha del historial médico")
    paciente_id: int = Field(..., description="ID del paciente asociado al historial médico")

    @field_validator("descripcion", "fecha", "paciente_id", mode="before", check_fields=True)
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value
    
    model_config: ClassVar[Dict[str, Any]] = {
        "json_schema_extra": {
            "examples": [
                {
                    "descripcion": "Historial médico de prueba",
                    "fecha": "2023-10-01T10:00:00",
                    "paciente_id": 1
                }
            ]
        }
    }

class HistorialMedicoCreate(HistorialMedicoBase):
    pass

class HistorialMedicoResponse(HistorialMedicoBase):
    id: int

class HistorialMedicoUpdate(HistorialMedicoBase):
    pass

    class Config:
        from_attributes = True
