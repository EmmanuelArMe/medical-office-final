from pydantic import BaseModel, Field, field_validator

class EspecialidadBase(BaseModel):
    nombre: str = Field(..., description="Nombre de la especialidad")

    @field_validator("nombre", mode="before", check_fields=True)
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value

class EspecialidadCreate(EspecialidadBase):
    pass

class EspecialidadResponse(EspecialidadBase):
    id: int

class EspecialidadUpdate(BaseModel):
    nombre: str = Field(..., description="Nombre de la especialidad")

    @field_validator("nombre", mode="before", check_fields=True)
    def validate_required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"El campo '{info.field_name}' es obligatorio.")
        return value

    class Config:
        orm_mode = True
