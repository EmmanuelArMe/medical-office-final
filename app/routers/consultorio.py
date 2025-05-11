from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.consultorio import ConsultorioCreate, ConsultorioResponse
from app.services import consultorio as service
from app.db.database import SessionLocal
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/consultorios", response_model=ConsultorioResponse)
def crear_consultorio(consultorio: ConsultorioCreate, db: Session = Depends(get_db)):
    nuevo_consultorio = service.crear_consultorio(db, consultorio)
    return JSONResponse(
        content={"message": "Consultorio creado correctamente", "response": jsonable_encoder(nuevo_consultorio)},
        status_code=status.HTTP_201_CREATED
    )


@router.get("/consultorios/{consultorio_id}", response_model=ConsultorioResponse)
def obtener_consultorio_por_id(consultorio_id: int, db: Session = Depends(get_db)):
    consultorio = service.obtener_consultorio_por_id(db, consultorio_id)
    return JSONResponse(
        content={"message": "Consultorio obtenido correctamente", "response": jsonable_encoder(consultorio)},
        status_code=status.HTTP_200_OK
    )

@router.get("/consultorios", response_model=list[ConsultorioResponse])
def Obtener_consultorios(skip: int, limit: int, db: Session = Depends(get_db)):
    return JSONResponse(
        content={"message": "Lista de consultorios obtenida correctamente", "response": jsonable_encoder(service.obtener_consultorios(db, skip, limit))},
        status_code=status.HTTP_200_OK
    )


@router.delete("/consultorios/{consultorio_id}", response_model=ConsultorioResponse)
def eliminar_consultorio(consultorio_id: int, db: Session = Depends(get_db)):
    consultorio = service.eliminar_consultorio(db, consultorio_id)
    return JSONResponse(
        content={
            "message": f"Consultorio con ID {consultorio_id} eliminado correctamente",
            "response": jsonable_encoder(consultorio)
        },
        status_code=status.HTTP_200_OK
    )

@router.put("/consultorios/{consultorio_id}", response_model=ConsultorioResponse)
def actualizar_consultorio(consultorio_id: int, consultorio: ConsultorioCreate, db: Session = Depends(get_db)):
    consultorio_actualizado = service.actualizar_consultorio(db, consultorio_id, consultorio)
    return JSONResponse(
        content={
            "message": f"Consultorio con ID {consultorio_id} actualizado correctamente",
            "response": jsonable_encoder(consultorio_actualizado)
        }
    )
