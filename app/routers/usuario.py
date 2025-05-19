from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.services import usuario as service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/usuarios",
    response_model=UsuarioResponse,
    summary="Crear usuario",
    description="Crea un nuevo usuario en el sistema."
)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    nuevo_usuario = service.crear_usuario(db, usuario)
    return JSONResponse(
        content={"message": "Usuario creado correctamente", "response": jsonable_encoder(nuevo_usuario)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
    "/usuarios/{id}",
    response_model=UsuarioResponse,
    summary="Obtener usuario por ID",
    description="Obtiene un usuario por su ID."
)
def obtener_usuario_por_id(id: int, db: Session = Depends(get_db)):
    usuario = service.obtener_usuario_por_id(db, id)
    return JSONResponse(
        content={"message": "Usuario obtenido correctamente", "response": jsonable_encoder(usuario)},
        status_code=status.HTTP_200_OK
    )

@router.get(
    "/usuarios",
    response_model=list[UsuarioResponse],
    summary="Obtener lista de usuarios",
    description="Obtiene una lista de todos los usuarios paginada."
)
def obtener_usuarios(skip: int, limit: int, db: Session = Depends(get_db)):
    usuarios = service.obtener_usuarios(db, skip=skip, limit=limit)
    return JSONResponse(
        content={"message": "Lista de usuarios obtenida correctamente", "response": jsonable_encoder(usuarios)},
        status_code=status.HTTP_200_OK
    )

@router.put(
    "/usuarios/{id}",
    response_model=UsuarioResponse,
    summary="Actualizar usuario",
    description="Actualiza un usuario por su ID."
)
def actualizar_usuario(id: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_actualizado = service.actualizar_usuario(db, id, usuario)
    return JSONResponse(
        content={"message": "Usuario actualizado correctamente", "response": jsonable_encoder(usuario_actualizado)},
        status_code=status.HTTP_200_OK
    )

@router.delete(
    "/usuarios/{id}",
    response_model=UsuarioResponse,
    summary="Eliminar usuario",
    description="Elimina un usuario por su ID."
)
def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = service.eliminar_usuario(db, id)
    return JSONResponse(
        content={"message": "Usuario eliminado correctamente", "response": jsonable_encoder(usuario)},
        status_code=status.HTTP_200_OK
    )

@router.get(
    "/usuarios/rol/{id}",
    response_model=list[UsuarioResponse],
    summary="Obtener usuarios por rol",
    description="Obtiene una lista de usuarios por su rol."
)   
def obtener_usuarios_por_rol(id: int, db: Session = Depends(get_db)):
    usuarios = service.obtener_usuario_por_rol(db, id)
    return JSONResponse(
        content={"message": "Lista de usuarios por rol obtenida correctamente", "response": jsonable_encoder(usuarios)},
        status_code=status.HTTP_200_OK
    )