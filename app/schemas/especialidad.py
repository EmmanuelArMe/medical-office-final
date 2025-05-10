from pydantic import BaseModel

class EspecialidadBase(BaseModel):
    nombre: str

class EspecialidadCreate(EspecialidadBase):
    pass

class EspecialidadResponse(EspecialidadBase):
    id: int

    class Config:
        orm_mode = True
