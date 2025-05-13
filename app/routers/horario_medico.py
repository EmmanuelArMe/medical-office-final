from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.horario_medico import HorarioMedicoCreate, HorarioMedicoResponse, HorarioMedicoUpdate
from app.services import horario_medico as service
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
            "/horarios",
        response_model=HorarioMedicoResponse,
        summary="Crear horario médico",
        description="Crea un nuevo horario médico en el sistema."
)
def crear_horario(horario: HorarioMedicoCreate, db: Session = Depends(get_db)):
    nuevo_horario_medico = service.crear_Horario_medico(db, horario)
    return JSONResponse(
        content={
            "message": "Horario médico creado correctamente",
            "response": jsonable_encoder(nuevo_horario_medico)
        },
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/horarios/{id}",
        response_model=HorarioMedicoResponse,
        summary="Obtener Horario médico por ID",
        description="Obtiene un Horario médico por su ID."
)
def obtener_horario_medico_por_id(id: int, db: Session = Depends(get_db)):
    horario_medico = service.obtener_horario_por_id(db, id)
    return JSONResponse(
        content={
            "message": "Horario médico obtenido correctamente",
            "response": jsonable_encoder(horario_medico)
        },
        status_code=status.HTTP_200_OK
    )
@router.get(
        "/horarios",
        response_model=list[HorarioMedicoResponse],
        summary="Obtener lista de horarios médicos",
        description="Obtiene una lista de horarios médicos paginada.")
def obtener_horarios_medicos(skip: int, limit: int, db: Session = Depends(get_db)):
    return JSONResponse(
        content={
            "message": "Lista de horarios médicos obtenidos correctamente",
            "response": jsonable_encoder(service.obtener_horarios_medicos(db, skip, limit))
        },
        status_code=status.HTTP_200_OK)
@router.delete(
        "/horario/{id}",
        response_model=HorarioMedicoResponse,
        summary="Eliminar Horario médico",
        description="Elimina un Horario médico por su ID.")

def eliminar_horario_medico(id: int, db: Session = Depends(get_db)):
    horario_medico = service.eliminar_horario_medico(db, id)
    return JSONResponse(
        content={
            "message": "horario médico eliminado correctamente",
            "response": jsonable_encoder(horario_medico)
        }, 
        status_code=status.HTTP_200_OK
    )

@router.get("/horarios/{id}", response_model=HorarioMedicoResponse)
def obtener_horario(id: int, db: Session = Depends(get_db)):
    horario = service.obtener_horario_por_id(db, id)
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario
@router.put(
        "/horarios/{id}",
        response_model=HorarioMedicoResponse,
        summary="Actualizar horario médico",
        description="Actualiza un horario médico por su ID.")
def actualizar_horario(id: int, horario: HorarioMedicoUpdate, db: Session = Depends(get_db)):
    Horario_medico_actualizado = service.actualizar_Horario_medico(db, id, horario)
    if Horario_medico_actualizado:
        return JSONResponse(
            content={
                "message": f"Horario médico con el id {id} ha sido actualizado correctamente",
                "response": jsonable_encoder(Horario_medico_actualizado)
            },
            status_code=status.HTTP_200_OK
        )
@router.get(
        "/horario/paciente/{id}",
        response_model=list[HorarioMedicoResponse],
        summary="Obtener horarios médicos por ID de paciente",
        description="Obtiene una lista de horarios médicos por el ID del paciente.")
def obtener_horario_medicos_por_id_paciente(id: int, db: Session = Depends(get_db)):
    historial_medico = service.obtener_horario_medicos_por_id_paciente(db, id)
    return JSONResponse(
        content={
            "message": f"Lista de horario médicos del paciente con id {id}, obtenidos correctamente",
            "response": jsonable_encoder(historial_medico)
        },
        status_code=status.HTTP_200_OK
    )