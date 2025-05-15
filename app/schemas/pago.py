from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, ClassVar

class PagoBase(BaseModel):
    paciente_id: int = Field(..., description="ID del paciente asociado al pago")
    monto: float = Field(..., description="Monto del pago")
    fecha: str = Field(..., description="Fecha del pago")
    metodo_pago: str = Field(..., description="Método de pago utilizado")
    
    model_config: ClassVar[Dict[str, Any]] = {
        "json_schema_extra": {
            "examples": [
                {
                    "paciente_id": 1,
                    "monto": 100.0,
                    "fecha": "2023-10-01",
                    "metodo_pago": "Tarjeta de crédito"
                }
            ]
        }
    }
    
    @field_validator("paciente_id", "monto", "fecha", "metodo_pago", mode="before")
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value
    
class PagoCreate(PagoBase):
    pass

class PagoResponse(PagoBase):
    id: int

class PagoUpdate(PagoBase):
    
    class Config:
        orm_mode = True