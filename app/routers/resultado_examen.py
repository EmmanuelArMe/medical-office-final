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
        summary="Crear resultado_examen",
        description="Crea un nuevo resultado_examen en el sistema."
)
def crear_resultado_examen(resultado_examen: ResultadoExamenCreate, db: Session = Depends(get_db)):
    nuevo_resultado_examen = service.crear_resultado_examen(db, resultado_examen)
    return JSONResponse(
        content={"message": "Resultado_examen creado correctamente", "response": jsonable_encoder(nuevo_resultado_examen)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/resultado_examenes/{resultado_examen_id}",
        response_model=ResultadoExamenResponse,
        summary="Obtener resultado_examen por ID",
        description="Obtiene un resultado_examen por su ID."
)
def obtener_resultado_examen_por_id(resultado_examen_id: int, db: Session = Depends(get_db)):
    resultado_examen = service.obtener_resultado_examen_por_id(db, resultado_examen_id)
    return JSONResponse(
        content={"message": "Resultado_examen obtenido correctamente", "response": jsonable_encoder(resultado_examen)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/resultado_examenes",
        response_model=list[ResultadoExamenResponse],
        summary="Obtener resultado_examenes",
        description="Obtiene una lista de resultado_examenes paginada."
)
def obtener_resultado_examenes(skip: int, limit: int, db: Session = Depends(get_db)):
    resultado_examenes = service.obtener_resultados_examenes(db, skip=skip, limit=limit)
    return JSONResponse(
        content={"message": "Lista de resultado_examenes obtenida correctamente", "response": jsonable_encoder(resultado_examenes)},
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/resultado_examenes/{resultado_examen_id}",
        response_model=ResultadoExamenResponse,
        summary="Eliminar resultado_examen",
        description="Elimina un resultado_examen por su ID."
)
def eliminar_resultado_examen(resultado_examen_id: int, db: Session = Depends(get_db)):
    resultado_examen = service.eliminar_resultado_examen(db, resultado_examen_id)
    return JSONResponse(
        content={"message": "Resultado_examen eliminado correctamente", "response": jsonable_encoder(resultado_examen)},
        status_code=status.HTTP_200_OK
    )
@router.put(
        "/resultado_examenes/{resultado_examen_id}",
        response_model=ResultadoExamenResponse,
        summary="Actualizar resultado_examen",
        description="Actualiza un resultado_examen por su ID."
)
def actualizar_resultado_examen(resultado_examen_id: int, resultado_examen_data: ResultadoExamenUpdate, db: Session = Depends(get_db)):
    resultado_examen_actualizado = service.actualizar_resultado_examen(db, resultado_examen_id, resultado_examen_data)
    return JSONResponse(
        content={"message": "Resultado_examen actualizado correctamente", "response": jsonable_encoder(resultado_examen_actualizado)},
        status_code=status.HTTP_200_OK
    )