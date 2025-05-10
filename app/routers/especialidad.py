from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
#from fastapi.encoders import jsonable_encoder
from app.db.database import SessionLocal
from app.schemas.especialidad import EspecialidadCreate, EspecialidadResponse
from app.services import especialidad as service
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/especialidades", response_model=EspecialidadResponse, status_code=status.HTTP_201_CREATED)
def crear_especialidad(especialidad: EspecialidadCreate, db: Session = Depends(get_db)):
    especialidad_creada = service.crear_especialidad(db, especialidad)
    return JSONResponse(
        content={"message": "Especialidad creada correctamente", "response": jsonable_encoder(especialidad_creada)},
        status_code=status.HTTP_201_CREATED
    )
@router.get("/especialidades", response_model=list[EspecialidadResponse])
def listar_especialidades(db: Session = Depends(get_db)):
    return service.obtener_especialidades(db)

@router.get("/especialidades/{id}", response_model=EspecialidadResponse)
def obtener_especialidad(id: int, db: Session = Depends(get_db)):
    especialidad = service.obtener_especialidad_por_id(db, id)
    if not especialidad:
        return JSONResponse(
            content={"message": f"La especialidad con ID {id} no fue encontrada"},
            status_code=status.HTTP_404_NOT_FOUND
        )
    return especialidad

@router.delete("/especialidades/{id}", response_model=EspecialidadResponse)
def eliminar_especialidad(id: int, db: Session = Depends(get_db)):
    especialidad = service.eliminar_especialidad(db, id)
    if not especialidad:
        return JSONResponse(
            content={"message": f"No se encontró una especialidad con ID {id}"},
            status_code=status.HTTP_404_NOT_FOUND
        )
    return especialidad
