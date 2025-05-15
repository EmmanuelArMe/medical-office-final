from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, ClassVar

class MedicamentoBase(BaseModel):
    nombre: str = Field(..., description="Nombre del medicamento")
    descripcion: str = Field(..., description="Descripción del medicamento")
    precio: float = Field(..., description="Precio del medicamento")
    cantidad_disponible: int = Field(..., description="Cantidad disponible en inventario")

    @field_validator("nombre", "descripcion", "precio", "cantidad_disponible", mode="before")
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value

    model_config: ClassVar[Dict[str, Any]] = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Paracetamol",
                    "descripcion": "Analgésico y antipirético",
                    "precio": 10.0,
                    "cantidad_disponible": 100
                }
            ]
        }
    }

class MedicamentoCreate(MedicamentoBase):
    pass

class MedicamentoResponse(MedicamentoBase):
    id: int

class MedicamentoUpdate(MedicamentoBase):
    
    class Config:
        orm_mode = True