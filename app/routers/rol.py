from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.rol import RolCreate, RolResponse, RolUpdate
from app.services import rol as service
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
        "/roles",
        response_model=RolResponse,
        summary="Crear rol",
        description="Crea un nuevo rol en el sistema."
)
def crear_rol(rol: RolCreate, db: Session = Depends(get_db)):
    nuevo_rol = service.crear_rol(db, rol)
    return JSONResponse(
        content={"message": "rol creado correctamente", "response": jsonable_encoder(nuevo_rol)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/roles/{id}",
        response_model=RolResponse,
        summary="Obtener rol por ID",
        description="Obtiene un rol por su ID."
)
def obtener_rol_por_id(id: int, db: Session = Depends(get_db)):
    rol = service.obtener_rol_por_id(db, id)
    return JSONResponse(
        content={"message": "rol obtenido correctamente", "response": jsonable_encoder(rol)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/roles",
        response_model=list[RolResponse],
        summary="Obtener lista de roles",
        description="Obtiene una lista de roles paginada."
)
def obtener_roles(skip: int, limit: int, db: Session = Depends(get_db)):
    roles = service.obtener_roles(db, skip=skip, limit=limit)
    return JSONResponse(
        content={"message": "Lista de roles obtenida correctamente", "response": jsonable_encoder(roles)},
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/roles/{id}",
        response_model=RolResponse,
        summary="Eliminar rol",
        description="Elimina un rol por su ID."
)
def eliminar_rol(id: int, db: Session = Depends(get_db)):
    rol = service.eliminar_rol(db, id)
    return JSONResponse(
        content={"message": f"rol con ID {id} eliminado correctamente", "response": jsonable_encoder(rol)},
        status_code=status.HTTP_200_OK
    )

@router.put(
        "/roles/{id}",
        response_model=RolResponse,
        summary="Actualizar rol",
        description="Actualiza un rol por su ID."
)
def actualizar_rol(id: int, rol: RolUpdate, db: Session = Depends(get_db)):
    rol_actualizado = service.actualizar_rol(db, id, rol)
    return JSONResponse(
        content={"message": f"rol con ID {id} actualizado correctamente", "response": jsonable_encoder(rol_actualizado)},
        status_code=status.HTTP_200_OK
    )