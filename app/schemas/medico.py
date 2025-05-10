from pydantic import BaseModel, EmailStr
from typing import Optional

class MedicoBase(BaseModel):
    nombre: str
    apellido: str
    especialidad_id: int
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None

class MedicoCreate(MedicoBase):
    pass

class MedicoResponse(MedicoBase):
    id: int

    class Config:
        from_attributes = True
