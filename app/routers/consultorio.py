from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.schemas.consultorio import ConsultorioCreate, ConsultorioResponse, ConsultorioUpdate
from app.services import consultorio as service
from app.db.database import get_db # Corrected import
from app.utils.auth import get_current_user
from app.models.usuario import Usuario # For type hinting current_user


router = APIRouter()

# Removed local get_db definition

@router.post(
        "/consultorios",
        response_model=ConsultorioResponse,
        summary="Crear consultorio",
        description="Crea un nuevo consultorio en el sistema."
)
def crear_consultorio(consultorio: ConsultorioCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    nuevo_consultorio = service.crear_consultorio(db, consultorio)
    return JSONResponse(
        content={"message": "Consultorio creado correctamente", "response": jsonable_encoder(nuevo_consultorio)},
        status_code=status.HTTP_201_CREATED
    )


@router.get(
        "/consultorios/{id}",
        response_model=ConsultorioResponse,
        summary="Obtener consultorio por ID",
        description="Obtiene un consultorio por su ID."
)
def obtener_consultorio_por_id(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    consultorio = service.obtener_consultorio_por_id(db, id)
    return JSONResponse(
        content={"message": "Consultorio obtenido correctamente", "response": jsonable_encoder(consultorio)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/consultorios",
        response_model=list[ConsultorioResponse],
        summary="Obtener lista de consultorios",
        description="Obtiene una lista de consultorios paginada."
)
def Obtener_consultorios(skip: int, limit: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return JSONResponse(
        content={"message": "Lista de consultorios obtenida correctamente", "response": jsonable_encoder(service.obtener_consultorios(db, skip, limit))},
        status_code=status.HTTP_200_OK
    )


@router.delete(
        "/consultorios/{id}",
        response_model=ConsultorioResponse,
        summary="Eliminar consultorio",
        description="Elimina un consultorio por su ID."
)
def eliminar_consultorio(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    consultorio = service.eliminar_consultorio(db, id)
    return JSONResponse(
        content={
            "message": f"Consultorio con ID {id} eliminado correctamente",
            "response": jsonable_encoder(consultorio)
        },
        status_code=status.HTTP_200_OK
    )

@router.put(
        "/consultorios/{id}",
        response_model=ConsultorioResponse,
        summary="Actualizar consultorio",
        description="Actualiza un consultorio por su ID."
)
def actualizar_consultorio(id: int, consultorio: ConsultorioUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    consultorio_actualizado = service.actualizar_consultorio(db, id, consultorio)
    return JSONResponse(
        content={
            "message": f"Consultorio con ID {id} actualizado correctamente",
            "response": jsonable_encoder(consultorio_actualizado)
        }
    )
