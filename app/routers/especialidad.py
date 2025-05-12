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
    nueva_especialidad = service.crear_especialidad(db, especialidad)
    return JSONResponse(
        content={"message": "Especialidad creada correctamente", "response": jsonable_encoder(nueva_especialidad)},
        status_code=status.HTTP_201_CREATED
    )


@router.get("/especialidades", response_model=list[EspecialidadResponse])
def obtener_especialidades(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    especialidades = service.obtener_especialidades(db, skip=skip, limit=limit)
    return JSONResponse(
        content={"message": "Lista de especialidades obtenida correctamente", "response": jsonable_encoder(especialidades)},
        status_code=status.HTTP_200_OK
    )

@router.get("/especialidades/{especialidad_id}", response_model=EspecialidadResponse)
def obtener_especialidad_por_id(especialidad_id: int, db: Session = Depends(get_db)):
    especialidad = service.obtener_especialidad_por_id(db, especialidad_id)
    return JSONResponse(
        content={"message": "Especialidad obtenida correctamente", "response": jsonable_encoder(especialidad)},
        status_code=status.HTTP_200_OK
    )


@router.delete("/especialidades/{especialidad_id}", response_model=EspecialidadResponse)
def eliminar_especialidad(especialidad_id: int, db: Session = Depends(get_db)):
    especialidad_eliminada = service.eliminar_especialidad(db, especialidad_id)
    return JSONResponse(
        content={"message": f"Especialidad con ID {especialidad_id} eliminada correctamente", "response": jsonable_encoder(especialidad_eliminada)},
        status_code=status.HTTP_200_OK
    )

@router.put("/especialidades/{especialidad_id}", response_model=EspecialidadResponse)
def actualizar_especialidad(especialidad_id: int, especialidad: EspecialidadCreate, db: Session = Depends(get_db)):
    especialidad_actualizada = service.actualizar_especialidad(db, especialidad_id, especialidad)
    return JSONResponse(
        content={"message": f"Especialidad con ID {especialidad_id} actualizada correctamente", "response": jsonable_encoder(especialidad_actualizada)},
        status_code=status.HTTP_200_OK
    )