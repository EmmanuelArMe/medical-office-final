from pydantic import BaseModel, Field, field_validator

class DiagnosticoBase(BaseModel):
    descripcion: str = Field(..., description="Descripción del diagnóstico")
    cita_id: int = Field(..., description="ID de la cita asociada al diagnóstico")

    @field_validator("descripcion", "cita_id", mode="before", check_fields=True)
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value

class DiagnosticoCreate(DiagnosticoBase):
    pass

class DiagnosticoResponse(DiagnosticoBase):
    id: int

class DiagnosticoUpdate(BaseModel):
    descripcion: str = Field(..., description="Descripción del diagnóstico")
    cita_id: int = Field(..., description="ID de la cita asociada al diagnóstico")

    @field_validator("descripcion", "cita_id", mode="before", check_fields=True)
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value

    class Config:
        from_attributes = True
