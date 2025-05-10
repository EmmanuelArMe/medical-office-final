from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.historial_medico import *
from app.services import historial_medico as service
from fastapi.responses import JSONResponse
#from fastapi.encoders import jsonable_encoder

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/historiales", response_model=list[HistorialMedicoResponse])
def listar_historiales(db: Session = Depends(get_db)):
    return service.obtener_historiales(db)

@router.get("/historiales/{id}", response_model=HistorialMedicoResponse)
def obtener_historial(id: int, db: Session = Depends(get_db)):
    historial = service.obtener_historial(db, id)
    if historial:
        return historial
    return JSONResponse(status_code=404, content={"message": "Historial médico no encontrado"})

@router.post("/historiales", response_model=HistorialMedicoResponse, status_code=status.HTTP_201_CREATED)
def crear_historial(historial: HistorialMedicoCreate, db: Session = Depends(get_db)):
    return service.crear_historial(db, historial)

@router.put("/historiales/{id}", response_model=HistorialMedicoResponse)
def actualizar_historial(id: int, historial: HistorialMedicoUpdate, db: Session = Depends(get_db)):
    actualizado = service.actualizar_historial(db, id, historial)
    if actualizado:
        return actualizado
    return JSONResponse(status_code=404, content={"message": "Historial médico no encontrado"})

@router.delete("/historiales/{id}", response_model=HistorialMedicoResponse)
def eliminar_historial(id: int, db: Session = Depends(get_db)):
    eliminado = service.eliminar_historial(db, id)
    if eliminado:
        return eliminado
    return JSONResponse(status_code=404, content={"message": "Historial médico no encontrado"})
