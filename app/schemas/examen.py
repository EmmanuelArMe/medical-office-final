from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, ClassVar

class ExamenBase(BaseModel):
    nombre: str = Field(..., description="Nombre del examen")
    descripcion: str = Field(None, description="Descripción del examen")

    @field_validator("nombre", "descripcion", mode="before", check_fields=True)
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value
    
    model_config: ClassVar[Dict[str, Any]] = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Examen de sangre",
                    "descripcion": "Examen para analizar los componentes de la sangre"
                }
            ]
        }
    }
    
class ExamenCreate(ExamenBase):
    pass

class ExamenResponse(ExamenBase):
    id: int

class ExamenUpdate(ExamenBase):
    pass

    class Config:
        orm_mode = True