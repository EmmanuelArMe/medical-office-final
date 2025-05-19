from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, ClassVar

class ResultadoExamenBase(BaseModel):
    paciente_id: int = Field(..., description="ID del paciente")
    examen_id: int = Field(..., description="ID del examen")
    resultado: str = Field(..., description="Resultado del examen")
    fecha_realizacion: str = Field(..., description="Fecha de realización del examen")
    
    @field_validator("paciente_id", "examen_id", "resultado", "fecha_realizacion", mode="before")
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value
    
    model_config: ClassVar[Dict[str, Any]] = {
        "json_schema_extra": {
            "examples": [
                {
                    "paciente_id": 1,
                    "examen_id": 1,
                    "resultado": "Normal",
                    "fecha_realizacion": "2023-10-01"
                }
            ]
        }
    }
    
class ResultadoExamenCreate(ResultadoExamenBase):
    pass

class ResultadoExamenResponse(ResultadoExamenBase):
    id: int

class ResultadoExamenUpdate(ResultadoExamenBase):
    
    class Config:
        orm_mode = True