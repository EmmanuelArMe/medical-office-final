from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, ClassVar

class RecetaBase(BaseModel):
    id: int = Field(..., description="ID de la receta")
    cita_id: int = Field(..., description="ID de la cita asociada a la receta")
    instrucciones: str = Field(..., description="Instrucciones para el paciente")
    
    model_config: ClassVar[Dict[str, Any]] = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "cita_id": 1,
                    "instrucciones": "Tomar 1 tableta al día"
                }
            ]
        }
    }
    
    @field_validator("id", "cita_id", "instrucciones", mode="before")
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value
    
class RecetaCreate(RecetaBase):
    pass

class RecetaResponse(RecetaBase):
    id: int

class RecetaUpdate(RecetaBase):
    
    class Config:
        orm_mode = True