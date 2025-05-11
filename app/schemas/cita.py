from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class CitaBase(BaseModel):
    fecha: datetime
    paciente_id: int = Field(..., description="ID del paciente")
    medico_id: int = Field(..., description="ID del médico")
    consultorio_id: int = Field(..., description="ID del consultorio")
    motivo: str = Field(..., description="Motivo de la cita")

    @field_validator("paciente_id", "medico_id", "consultorio_id", "motivo", mode="before", check_fields=True)
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value

class CitaCreate(CitaBase):
    pass

class CitaResponse(CitaBase):
    id: int

class CitaUpdate(BaseModel):
    fecha: datetime | None = Field(None, description="Fecha de la cita")
    paciente_id: int | None = Field(None, description="ID del paciente")
    medico_id: int | None = Field(None, description="ID del médico")
    consultorio_id: int | None = Field(None, description="ID del consultorio")
    motivo: str | None = Field(None, description="Motivo de la cita")

    @field_validator("paciente_id", "medico_id", "consultorio_id", "motivo", mode="before", check_fields=True)
    def validate_required_fields(cls, value, info):
        if value is 0 or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio y debe ser distinto de 0 o vacio.")
        return value

    class Config:
        from_attributes = True