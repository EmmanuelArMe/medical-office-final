from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.resultado_examen import ResultadoExamenCreate, ResultadoExamenResponse, ResultadoExamenUpdate
from app.services import resultado_examen as service
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
        "/resultado_examenes",
        response_model=ResultadoExamenResponse,
        summary="Crear resultado de examen",
        description="Crea un nuevo resultado de examen en el sistema."
)
def crear_resultado_examen(resultado_examen: ResultadoExamenCreate, db: Session = Depends(get_db)):
    nuevo_resultado_examen = service.crear_resultado_examen(db, resultado_examen)
    return JSONResponse(
        content={"message": "Resultado de examen creado correctamente", "response": jsonable_encoder(nuevo_resultado_examen)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/resultado_examenes/{id}",
        response_model=ResultadoExamenResponse,
        summary="Obtener resultado de examen por ID",
        description="Obtiene un resultado de examen por su ID."
)
def obtener_resultado_examen_por_id(id: int, db: Session = Depends(get_db)):
    resultado_examen = service.obtener_resultado_examen_por_id(db, id)
    return JSONResponse(
        content={"message": "Resultado de examen obtenido correctamente", "response": jsonable_encoder(resultado_examen)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/resultado_examenes",
        response_model=list[ResultadoExamenResponse],
        summary="Obtener lista de resultados de examenes",
        description="Obtiene una lista de resultados de examenes paginada."
)
def obtener_resultado_examenes(skip: int, limit: int, db: Session = Depends(get_db)):
    resultado_examenes = service.obtener_resultados_examenes(db, skip=skip, limit=limit)
    return JSONResponse(
        content={"message": "Lista de resultados de examenes obtenida correctamente", "response": jsonable_encoder(resultado_examenes)},
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/resultado_examenes/{id}",
        response_model=ResultadoExamenResponse,
        summary="Eliminar resultado de examen",
        description="Elimina un resultado de examen por su ID."
)
def eliminar_resultado_examen(id: int, db: Session = Depends(get_db)):
    resultado_examen = service.eliminar_resultado_examen(db, id)
    return JSONResponse(
        content={"message": "Resultado de examen eliminado correctamente", "response": jsonable_encoder(resultado_examen)},
        status_code=status.HTTP_200_OK
    )
@router.put(
        "/resultado_examenes/{id}",
        response_model=ResultadoExamenResponse,
        summary="Actualizar resultado de examen",
        description="Actualiza un resultado de examen por su ID."
)
def actualizar_resultado_examen(id: int, resultado_examen_data: ResultadoExamenUpdate, db: Session = Depends(get_db)):
    resultado_examen_actualizado = service.actualizar_resultado_examen(db, id, resultado_examen_data)
    return JSONResponse(
        content={"message": "Resultado de examen actualizado correctamente", "response": jsonable_encoder(resultado_examen_actualizado)},
        status_code=status.HTTP_200_OK
    )
    
@router.get(
        "/resultado_examenes/paciente/{id}",
        response_model=list[ResultadoExamenResponse],
        summary="Obtener resultado de examen por paciente",
        description="Obtiene un resultado de examen por el ID del paciente."
)
def obtener_resultados_examenes_por_paciente(id: int, db: Session = Depends(get_db)):
    resultado_examenes = service.obtener_resultados_examenes_por_paciente(db, id)
    return JSONResponse(
        content={"message": "Resultados de examenes obtenidos correctamente", "response": jsonable_encoder(resultado_examenes)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/resultado_examenes/examen/{id}",
        response_model=list[ResultadoExamenResponse],
        summary="Obtener resultado de examen por examen",
        description="Obtiene una lista de resultados de examen por el ID del examen."
)
def obtener_resultados_examenes_por_examen(id: int, db: Session = Depends(get_db)):
    resultado_examenes = service.obtener_resultados_examenes_por_examen(db, id)
    return JSONResponse(
        content={"message": "Resultados de examenes obtenidos correctamente", "response": jsonable_encoder(resultado_examenes)},
        status_code=status.HTTP_200_OK
    )