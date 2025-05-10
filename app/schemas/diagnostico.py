from pydantic import BaseModel
# from typing import Optional

class DiagnosticoBase(BaseModel):
    descripcion: str
    cita_id: int

class DiagnosticoCreate(DiagnosticoBase):
    pass

class DiagnosticoResponse(DiagnosticoBase):
    id: int

    class Config:
        from_attributes = True
