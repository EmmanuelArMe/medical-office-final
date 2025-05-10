from pydantic import BaseModel

class ConsultorioBase(BaseModel):
    nombre: str
    piso: int

class ConsultorioCreate(ConsultorioBase):
    pass

class ConsultorioResponse(ConsultorioBase):
    id: int

    class Config:
        orm_mode = True