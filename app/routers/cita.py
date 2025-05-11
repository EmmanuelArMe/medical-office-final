from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.schemas.cita import CitaCreate, CitaResponse, CitaUpdate
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
def obtener_cita_por_id(cita_id: int, db: Session = Depends(get_db)):
    cita = service.obtener_cita_por_id(db, cita_id)
    return JSONResponse(
        content={"message": "Cita obtenida correctamente", "response": jsonable_encoder(cita)},
        status_code=status.HTTP_200_OK
    )

@router.get("/citas", response_model=list[CitaResponse])
def obtener_citas(skip: int, limit: int, db: Session = Depends(get_db)):
    return JSONResponse( 
        content={"message": "Lista de citas obtenida correctamente", "response": jsonable_encoder(service.obtener_citas(db, skip, limit))},
        status_code=status.HTTP_200_OK
    )

@router.delete("/citas/{cita_id}")
def eliminar_cita(cita_id: int, db: Session = Depends(get_db)):
    service.eliminar_cita(db, cita_id)
    return JSONResponse(
        content={
            "message": f"Cita con ID {cita_id} eliminada correctamente"
        },
        status_code=status.HTTP_200_OK
    )


@router.put("/citas/{cita_id}", response_model=CitaResponse)
def actualizar_cita(cita_id: int, cita: CitaUpdate, db: Session = Depends(get_db)):
    cita_actualizada = service.actualizar_cita(db, cita_id, cita)
    return JSONResponse(
        content={
            "message": f"Cita con ID {cita_id} actualizada correctamente",
            "response": jsonable_encoder(cita_actualizada)
        },
        status_code=status.HTTP_200_OK
    )

@router.get("/citas/paciente/{paciente_id}", response_model=list[CitaResponse])
def obtener_citas_por_paciente(paciente_id: int, db: Session = Depends(get_db)):
    citas_por_paciente = service.obtener_citas_por_paciente(db, paciente_id)
    return JSONResponse(
        content={
            "message": f"Citas obtenidas correctamente para el paciente con ID {paciente_id}",
            "response": jsonable_encoder(citas_por_paciente)
        },
        status_code=status.HTTP_200_OK
    )

@router.get("/citas/medico/{medico_id}", response_model=list[CitaResponse])
def obtener_citas_por_medico(medico_id: int, db: Session = Depends(get_db)):
    citas_por_medico = service.obtener_citas_por_medico(db, medico_id)
    return JSONResponse(
        content={
            "message": f"Citas obtenidas correctamente para el médico con ID {medico_id}",
            "response": jsonable_encoder(citas_por_medico)
        },
        status_code=status.HTTP_200_OK
    )

@router.get("/citas/consultorio/{consultorio_id}", response_model=list[CitaResponse])
def obtener_citas_por_consultorio(consultorio_id: int, db: Session = Depends(get_db)):
    citas_por_consultorio = service.obtener_citas_por_consultorio(db, consultorio_id)
    return JSONResponse(
        content={
            "message": f"Citas obtenidas correctamente para el consultorio con ID {consultorio_id}",
            "response": jsonable_encoder(citas_por_consultorio)
        },
        status_code=status.HTTP_200_OK
    )

@router.get("/citas/fecha/{fecha}", response_model=list[CitaResponse])
def obtener_citas_por_fecha(fecha: str, db: Session = Depends(get_db)):
    citas_por_fecha = service.obtener_citas_por_fecha(db, fecha)
    return JSONResponse(
        content={
            "message": f"Citas obtenidas correctamente para la fecha {fecha}",
            "response": jsonable_encoder(citas_por_fecha)
        },
        status_code=status.HTTP_200_OK
    )