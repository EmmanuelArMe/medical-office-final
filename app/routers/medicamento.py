from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.db.database import get_db # Corrected import
from app.schemas.medicamento import MedicamentoCreate, MedicamentoResponse, MedicamentoUpdate
from app.services import medicamento as service
from app.utils.auth import get_current_user
from app.models.usuario import Usuario # For type hinting current_user

router = APIRouter()

# Removed local get_db definition

@router.post(
        "/medicamentos",
        response_model=MedicamentoResponse,
        summary="Crear medicamento",
        description="Crea un nuevo medicamento en el sistema."
)
def crear_medicamento(medicamento: MedicamentoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    nuevo_medicamento = service.crear_medicamento(db, medicamento)
    return JSONResponse(
        content={"message": "Medicamento creado correctamente", "response": jsonable_encoder(nuevo_medicamento)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/medicamentos/{id}",
        response_model=MedicamentoResponse,
        summary="Obtener medicamento por ID",
        description="Obtiene un medicamento por su ID."
)
def obtener_medicamento_por_id(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    medicamento = service.obtener_medicamento_por_id(db, id)
    return JSONResponse(
        content={"message": "Medicamento obtenido correctamente", "response": jsonable_encoder(medicamento)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/medicamentos",
        response_model=list[MedicamentoResponse],
        summary="Obtener lista de medicamentos",
        description="Obtiene una lista de medicamentos paginada."
)
def obtener_medicamentos(skip: int, limit: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    medicamentos = service.obtener_medicamentos(db, skip=skip, limit=limit)
    return JSONResponse(
        content={"message": "Lista de medicamentos obtenida correctamente", "response": jsonable_encoder(medicamentos)},
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/medicamentos/{id}",
        response_model=MedicamentoResponse,
        summary="Eliminar medicamento",
        description="Elimina un medicamento por su ID."
)
def eliminar_medicamento(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    medicamento = service.eliminar_medicamento(db, id)
    return JSONResponse(
        content={"message": "Medicamento eliminado correctamente", "response": jsonable_encoder(medicamento)},
        status_code=status.HTTP_200_OK
    )
@router.put(
        "/medicamentos/{id}",
        response_model=MedicamentoResponse,
        summary="Actualizar medicamento",
        description="Actualiza un medicamento por su ID."
)
def actualizar_medicamento(id: int, medicamento_data: MedicamentoUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    medicamento_actualizado = service.actualizar_medicamento(db, id, medicamento_data)
    return JSONResponse(
        content={"message": "Medicamento actualizado correctamente", "response": jsonable_encoder(medicamento_actualizado)},
        status_code=status.HTTP_200_OK
    )