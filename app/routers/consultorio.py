from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.consultorio import ConsultorioCreate, ConsultorioResponse
from app.services import consultorio as service
from app.db.database import SessionLocal
from fastapi.encoders import jsonable_encoder
#from fastapi.encoders import jsonable_encoder

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/consultorios", response_model=ConsultorioResponse)
def crear_consultorio(consultorio: ConsultorioCreate, db: Session = Depends(get_db)):
    nuevo = service.crear_consultorio(db, consultorio)
    return JSONResponse(
        content={
            "message": "Consultorio creado correctamente",
            "response": jsonable_encoder(nuevo)
        },
        status_code=status.HTTP_201_CREATED
    )


@router.get("/consultorios", response_model=list[ConsultorioResponse])
def listar_consultorios(db: Session = Depends(get_db)):
    return service.listar_consultorios(db)

@router.get("/consultorios/{consultorio_id}", response_model=ConsultorioResponse)
def obtener_consultorio(consultorio_id: int, db: Session = Depends(get_db)):
    consultorio = service.obtener_consultorio(db, consultorio_id)
    if not consultorio:
        return JSONResponse(
            content={"message": f"Consultorio con ID {consultorio_id} no encontrado."},
            status_code=status.HTTP_404_NOT_FOUND
        )
    return consultorio

@router.delete("/consultorios/{consultorio_id}", response_model=ConsultorioResponse)
def eliminar_consultorio(consultorio_id: int, db: Session = Depends(get_db)):
    consultorio = service.eliminar_consultorio(db, consultorio_id)
    if not consultorio:
        return JSONResponse(
            content={"message": f"Consultorio con ID {consultorio_id} no encontrado."},
            status_code=status.HTTP_404_NOT_FOUND
        )
    return consultorio
