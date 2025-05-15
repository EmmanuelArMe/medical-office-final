from pydantic import BaseModel, Field, field_validator
from datetime import time
from typing import ClassVar, Dict, Any

class HorarioMedicoBase(BaseModel):
    medico_id: int = Field(..., description="ID del médico")
    dia_semana: str = Field(..., description="Día de la semana")
    hora_inicio: time = Field(..., description="Hora de inicio del horario")
    hora_fin: time = Field(..., description="Hora de fin del horario")

    @field_validator("medico_id", "dia_semana", "hora_inicio", "hora_fin", mode="before", check_fields=True)
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value
    
    model_config: ClassVar[Dict[str, Any]] = {
        "json_schema_extra": {
            "examples": [
                {
                    "medico_id": 1,
                    "dia_semana": "Lunes",
                    "hora_inicio": "09:00:00",
                    "hora_fin": "17:00:00"
                }
            ]
        }
    }

class HorarioMedicoCreate(HorarioMedicoBase):
    pass

class HorarioMedicoResponse(HorarioMedicoBase):
    id: int

class HorarioMedicoUpdate(HorarioMedicoBase):
    pass

    class Config:
        orm_mode = True
