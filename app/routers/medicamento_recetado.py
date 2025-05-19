from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.schemas.medicamento_recetado import MedicamentoRecetadoCreate, MedicamentoRecetadoResponse, MedicamentoRecetadoUpdate
from app.services import medicamento_recetado as service
from app.db.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
        "/medicamentos_recetados",
        response_model=MedicamentoRecetadoResponse,
        summary="Crear medicamento recetado",
        description="Crea un nuevo medicamento recetado en el sistema."
)
def crear_medicamento_recetado(medicamento_recetado: MedicamentoRecetadoCreate, db: Session = Depends(get_db)):
    nuevo_medicamento_recetado = service.crear_medicamento_recetado(db, medicamento_recetado)
    return JSONResponse(
        content={"message": "Medicamento recetado creado correctamente", "response": jsonable_encoder(nuevo_medicamento_recetado)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/medicamentos_recetados/{id}",
        response_model=MedicamentoRecetadoResponse,
        summary="Obtener medicamento recetado por ID",
        description="Obtiene un medicamento recetado por su ID."
)
def obtener_medicamento_recetado_por_id(id: int, db: Session = Depends(get_db)):
    medicamento_recetado = service.obtener_medicamento_recetado_por_id(db, id)
    return JSONResponse(
        content={"message": "Medicamento recetado obtenido correctamente", "response": jsonable_encoder(medicamento_recetado)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/medicamentos_recetados",
        response_model=list[MedicamentoRecetadoResponse],
        summary="Obtener lista de medicamentos recetados",
        description="Obtiene una lista de medicamentos recetados paginada."
)
def obtener_medicamentos_recetados(skip: int, limit: int, db: Session = Depends(get_db)):
    return JSONResponse( 
        content={"message": "Lista de medicamentos recetados obtenida correctamente", "response": jsonable_encoder(service.obtener_medicamentos_recetados(db, skip, limit))},
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/medicamentos_recetados/{id}",
        response_model=MedicamentoRecetadoResponse,
        summary="Eliminar medicamento recetado",
        description="Elimina un medicamento recetado por su ID."
)
def eliminar_medicamento_recetado(id: int, db: Session = Depends(get_db)):
    medicamento_recetado = service.eliminar_medicamento_recetado(db, id)
    return JSONResponse(
        content={"message": "Medicamento recetado eliminado correctamente", "response": jsonable_encoder(medicamento_recetado)},
        status_code=status.HTTP_200_OK
    )

@router.put(
        "/medicamentos_recetados/{id}",
        response_model=MedicamentoRecetadoResponse,
        summary="Actualizar medicamento recetado",
        description="Actualiza un medicamento recetado por su ID."
)
def actualizar_medicamento_recetado(id: int, medicamento_recetado: MedicamentoRecetadoUpdate, db: Session = Depends(get_db)):
    medicamento_recetado_actualizado = service.actualizar_medicamento_recetado(db, id, medicamento_recetado)
    return JSONResponse(
        content={"message": "Medicamento recetado actualizado correctamente", "response": jsonable_encoder(medicamento_recetado_actualizado)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/medicamentos_recetados/receta/{id}",
        response_model=list[MedicamentoRecetadoResponse],
        summary="Obtener medicamentos recetados por receta",
        description="Obtiene una lista de medicamentos recetados por el ID de la receta."
)
def obtener_medicamentos_recetados_por_receta(id: int, db: Session = Depends(get_db)):
    medicamentos_recetados = service.obtener_medicamentos_recetados_por_receta(db, id)
    return JSONResponse(
        content={"message": "Lista de medicamentos recetados obtenida correctamente", "response": jsonable_encoder(medicamentos_recetados)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/medicamentos_recetados/medicamento/{id}",
        response_model=list[MedicamentoRecetadoResponse],
        summary="Obtener medicamentos recetados por medicamento",
        description="Obtiene una lista de medicamentos recetados por el ID del medicamento."
)
def obtener_medicamentos_recetados_por_medicamento(id: int, db: Session = Depends(get_db)):
    medicamentos_recetados = service.obtener_medicamentos_recetados_por_medicamento(db, id)
    return JSONResponse(
        content={"message": "Lista de medicamentos recetados obtenida correctamente", "response": jsonable_encoder(medicamentos_recetados)},
        status_code=status.HTTP_200_OK
    )