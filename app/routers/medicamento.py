from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.medicamento import MedicamentoCreate, MedicamentoResponse, MedicamentoUpdate
from app.services import medicamento as service
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
        "/medicamentos",
        response_model=MedicamentoResponse,
        summary="Crear medicamento",
        description="Crea un nuevo medicamento en el sistema."
)
def crear_medicamento(medicamento: MedicamentoCreate, db: Session = Depends(get_db)):
    nuevo_medicamento = service.crear_medicamento(db, medicamento)
    return JSONResponse(
        content={"message": "Medicamento creado correctamente", "response": jsonable_encoder(nuevo_medicamento)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/medicamentos/{medicamento_id}",
        response_model=MedicamentoResponse,
        summary="Obtener medicamento por ID",
        description="Obtiene un medicamento por su ID."
)
def obtener_medicamento_por_id(medicamento_id: int, db: Session = Depends(get_db)):
    medicamento = service.obtener_medicamento_por_id(db, medicamento_id)
    return JSONResponse(
        content={"message": "Medicamento obtenido correctamente", "response": jsonable_encoder(medicamento)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/medicamentos",
        response_model=list[MedicamentoResponse],
        summary="Obtener medicamentos",
        description="Obtiene una lista de medicamentos paginada."
)
def obtener_medicamentos(skip: int, limit: int, db: Session = Depends(get_db)):
    medicamentos = service.obtener_medicamentos(db, skip=skip, limit=limit)
    return JSONResponse(
        content={"message": "Lista de medicamentos obtenida correctamente", "response": jsonable_encoder(medicamentos)},
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/medicamentos/{medicamento_id}",
        response_model=MedicamentoResponse,
        summary="Eliminar medicamento",
        description="Elimina un medicamento por su ID."
)
def eliminar_medicamento(medicamento_id: int, db: Session = Depends(get_db)):
    medicamento = service.eliminar_medicamento(db, medicamento_id)
    return JSONResponse(
        content={"message": "Medicamento eliminado correctamente", "response": jsonable_encoder(medicamento)},
        status_code=status.HTTP_200_OK
    )
@router.put(
        "/medicamentos/{medicamento_id}",
        response_model=MedicamentoResponse,
        summary="Actualizar medicamento",
        description="Actualiza un medicamento por su ID."
)
def actualizar_medicamento(medicamento_id: int, medicamento_data: MedicamentoUpdate, db: Session = Depends(get_db)):
    medicamento_actualizado = service.actualizar_medicamento(db, medicamento_id, medicamento_data)
    return JSONResponse(
        content={"message": "Medicamento actualizado correctamente", "response": jsonable_encoder(medicamento_actualizado)},
        status_code=status.HTTP_200_OK
    )