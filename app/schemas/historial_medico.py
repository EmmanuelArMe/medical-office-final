from pydantic import BaseModel
from datetime import datetime

class HistorialMedicoBase(BaseModel):
    descripcion: str
    fecha: datetime
    paciente_id: int

class HistorialMedicoCreate(HistorialMedicoBase):
    pass

class HistorialMedicoUpdate(HistorialMedicoBase):
    pass

class HistorialMedicoResponse(HistorialMedicoBase):
    id: int

    class Config:
        from_attributes = True
