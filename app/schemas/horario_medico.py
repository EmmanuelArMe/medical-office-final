from pydantic import BaseModel
from datetime import time

class HorarioMedicoBase(BaseModel):
    medico_id: int
    dia_semana: str
    hora_inicio: time
    hora_fin: time

class HorarioMedicoCreate(HorarioMedicoBase):
    pass

class HorarioMedicoResponse(HorarioMedicoBase):
    id: int

    class Config:
        orm_mode = True
