from pydantic import BaseModel
from datetime import datetime

class CitaBase(BaseModel):
    fecha: datetime
    paciente_id: int
    medico_id: int
    consultorio_id: int
    motivo: str

class CitaCreate(CitaBase):
    pass

class CitaResponse(CitaBase):
    id: int

    class Config:
        from_attributes = True
