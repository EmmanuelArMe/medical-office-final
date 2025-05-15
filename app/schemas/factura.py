from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, ClassVar

class FacturaBase(BaseModel):
    pago_id : int = Field(..., description="ID del pago asociado a la factura")
    detalle : str = Field(..., description="Detalle de la factura")
    fecha_emision : str = Field(..., description="Fecha de emisión de la factura")

    @field_validator("pago_id", "detalle", "fecha_emision", mode="before", check_fields=True)
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value
    
    model_config: ClassVar[Dict[str, Any]] = {
        "json_schema_extra": {
            "examples": [
                {
                    "pago_id": 1,
                    "detalle": "Factura por servicios médicos",
                    "fecha_emision": "2023-10-01"
                }
            ]
        }
    }

class FacturaCreate(FacturaBase):
    pass

class FacturaResponse(FacturaBase):
    id: int

class FacturaUpdate(FacturaBase):
    pass

class Config:
    orm_mode = True