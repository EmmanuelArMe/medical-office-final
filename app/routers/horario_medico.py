from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.horario_medico import HorarioMedicoCreate, HorarioMedicoResponse
from app.services import horario_medico as service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/horarios", response_model=HorarioMedicoResponse)
def crear_horario(horario: HorarioMedicoCreate, db: Session = Depends(get_db)):
    return service.crear_horario_medico(db, horario)

@router.get("/horarios", response_model=list[HorarioMedicoResponse])
def listar_horarios(db: Session = Depends(get_db)):
    return service.obtener_horarios(db)

@router.get("/horarios/{id}", response_model=HorarioMedicoResponse)
def obtener_horario(id: int, db: Session = Depends(get_db)):
    horario = service.obtener_horario_por_id(db, id)
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario

@router.put("/horarios/{id}", response_model=HorarioMedicoResponse)
def actualizar_horario(id: int, horario: HorarioMedicoCreate, db: Session = Depends(get_db)):
    horario_actualizado = service.actualizar_horario_medico(db, id, horario.dict())
    if not horario_actualizado:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario_actualizado

@router.delete("/horarios/{id}", response_model=HorarioMedicoResponse)
def eliminar_horario(id: int, db: Session = Depends(get_db)):
    eliminado = service.eliminar_horario_medico(db, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return eliminado
