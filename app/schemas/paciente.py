from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional

    
class PacienteBase(BaseModel):
    nombre: str = Field(..., description="Nombre del paciente")
    apellido: str = Field(..., description="Apellido del paciente")
    fecha_nacimiento: date = Field(..., description="Fecha de nacimiento del paciente")
    documento: str = Field(..., description="Número de documento del paciente")
    telefono: str = Field(..., description="Número de teléfono del paciente")
    email: str = Field(..., description="Email del paciente")

    @field_validator("nombre", "apellido", "documento", "telefono", "email", mode="before", check_fields=True)
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value

class PacienteCreate(PacienteBase):
    pass

class PacienteResponse(PacienteBase):
    id: int
    nombre: str
    telefono: Optional[str] = None
    email: Optional[str] = None

class PacienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, description="Nombre del paciente")
    apellido: Optional[str] = Field(None, description="Apellido del paciente")
    fecha_nacimiento: Optional[date] = Field(None, description="Fecha de nacimiento del paciente")
    documento: Optional[str] = Field(None, description="Número de documento del paciente")
    telefono: Optional[str] = Field(None, description="Número de teléfono del paciente")
    email: Optional[str] = Field(None, description="Email del paciente")

    @field_validator("nombre", "apellido", "fecha_nacimiento", "documento", "telefono", "email", mode="before", check_fields=True)
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value

    class Config:
        orm_mode = True
        from_attributes = True
