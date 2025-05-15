from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, ClassVar

class MedicamentoRecetadoBase(BaseModel):
    receta_id: int = Field(..., description="ID de la receta asociada")
    medicamento_id: int = Field(..., description="ID del medicamento asociado")
    dosis: int = Field(..., description="Dosis del medicamento")

    @field_validator("receta_id", "medicamento_id", "dosis", mode="before")
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value

    model_config: ClassVar[Dict[str, Any]] = {
        "json_schema_extra": {
            "examples": [
                {
                    "receta_id": 1,
                    "medicamento_id": 2,
                    "dosis": 500
                }
            ]
        }
    }

class MedicamentoRecetadoCreate(MedicamentoRecetadoBase):
    pass

class MedicamentoRecetadoResponse(MedicamentoRecetadoBase):
    id: int

class MedicamentoRecetadoUpdate(MedicamentoRecetadoBase):

    class Config:
        orm_mode = True