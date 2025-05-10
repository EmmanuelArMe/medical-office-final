from pydantic import BaseModel
from datetime import date
from typing import Optional

    
class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: date
    documento: str
    telefono: str
    email: str

class PacienteCreate(PacienteBase):
    pass

class PacienteResponse(PacienteBase):
    id: int
    nombre: str
    telefono: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True
