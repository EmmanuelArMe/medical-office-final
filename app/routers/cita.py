from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.schemas.cita import CitaCreate, CitaResponse
from app.services import cita as service
from app.db.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/citas", response_model=CitaResponse)
def crear_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    nueva_cita = service.crear_cita(db, cita)
    return JSONResponse(
        content={"message": "Cita creada correctamente", "response": jsonable_encoder(nueva_cita)},
        status_code=status.HTTP_201_CREATED
    )

@router.get("/citas/{cita_id}", response_model=CitaResponse)
def obtener_cita(cita_id: int, db: Session = Depends(get_db)):
    cita = service.obtener_cita(db, cita_id)
    if not cita:
        return JSONResponse(
            content={"message": f"No se encontró la cita con ID {cita_id}"},
            status_code=status.HTTP_404_NOT_FOUND
        )
    return cita

@router.get("/citas", response_model=list[CitaResponse])
def listar_citas(db: Session = Depends(get_db)):
    return service.listar_citas(db)

@router.delete("/citas/{cita_id}", response_model=CitaResponse)
def eliminar_cita(cita_id: int, db: Session = Depends(get_db)):
    cita = service.eliminar_cita(db, cita_id)
    if not cita:
        return JSONResponse(
            content={"message": f"No se encontró la cita con ID {cita_id}"},
            status_code=status.HTTP_404_NOT_FOUND
        )
    return JSONResponse(
        content={
            "message": f"Cita con ID {cita_id} eliminada correctamente",
            "response": jsonable_encoder(cita)
        },
        status_code=status.HTTP_200_OK
    )
