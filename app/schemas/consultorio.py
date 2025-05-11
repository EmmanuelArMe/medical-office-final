from pydantic import BaseModel, Field, field_validator

class ConsultorioBase(BaseModel):
    nombre: str = Field(..., description="Nombre del consultorio")
    piso: int = Field(..., description="Piso del consultorio")

    @field_validator("nombre", "piso", mode="before", check_fields=True)
    def validate_required_fields(cls, value, info):
        if value is None or value == 0 or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio y debe ser distinto de 0 o vacio.")
        return value

class ConsultorioCreate(ConsultorioBase):
    pass

class ConsultorioResponse(ConsultorioBase):
    id: int

    class Config:
        orm_mode = True