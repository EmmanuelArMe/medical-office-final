from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.repositories import usuario as usuario_repository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def crear_usuario(db: Session, usuario: UsuarioCreate):
    usuario_existente = db.query(Usuario).filter(Usuario.username == usuario.username).first()
    if usuario_existente:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario con el username {usuario.username}"
        ) 
    # Verificar si el rol existe
    rol_existente = db.query(Rol).filter(Rol.id == usuario.rol_id).first()
    if not rol_existente:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El rol con ID {usuario.rol_id} no existe."
        )
    
    hashed_password = pwd_context.hash(usuario.password)
    usuario_data_for_repo = usuario.model_copy(update={"password": hashed_password})
    
    nuevo_usuario = usuario_repository.crear_usuario(db, usuario_data_for_repo)
    if not nuevo_usuario:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el usuario"
        )
    return nuevo_usuario

def obtener_usuario_por_id(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El usuario con ID {usuario_id} no fue encontrado."
        )
    return usuario_repository.obtener_usuario_por_id(db, usuario_id)

def obtener_usuario_por_nombre_de_usuario(db: Session, username: str) -> Usuario | None:
    return usuario_repository.obtener_usuario_por_username(db, username)

def obtener_usuarios(db: Session, skip: int, limit: int):
    usuarios = db.query(Usuario).all()
    if not usuarios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron usuarios."
        )
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a 0 y 1 respectivamente."
        )
    return usuario_repository.obtener_usuarios(db, skip, limit)

def eliminar_usuario(db: Session, usuario_id: int):
    usuario = obtener_usuario_por_id(db, usuario_id)
    usuario_repository.eliminar_usuario(db, usuario_id)
    return usuario

def actualizar_usuario(db: Session, usuario_id: int, usuario_data: UsuarioUpdate):
    usuario_db = obtener_usuario_por_id(db, usuario_id) # Renamed to avoid confusion with 'usuario_data'
    
    # Create a dictionary from usuario_data to allow modification
    update_data = usuario_data.model_dump(exclude_unset=True)

    if "password" in update_data and update_data["password"] is not None:
        hashed_password = pwd_context.hash(update_data["password"])
        update_data["password"] = hashed_password
    
    # Pass the modified dictionary (or a new UsuarioUpdate object if repository expects that)
    # For now, assuming repository can handle a dictionary or specific fields.
    # If repository strictly expects UsuarioUpdate, we might need:
    # updated_usuario_data_obj = UsuarioUpdate(**update_data)
    # usuario_actualizado = usuario_repository.actualizar_usuario(db, usuario_db, updated_usuario_data_obj)
    
    # Assuming repository's actualizar_usuario can take the db object, the model instance, and a dict of changes
    usuario_actualizado = usuario_repository.actualizar_usuario(db, usuario_db, UsuarioUpdate(**update_data))
    if not usuario_actualizado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el usuario"
        )
    return usuario_actualizado

def obtener_usuario_por_rol(db: Session, rol_id: int):
    usuarios = db.query(Usuario).filter(Usuario.rol_id == rol_id).all()
    if not usuarios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron usuarios con el rol ID {rol_id}."
        )
    return usuario_repository.obtener_usuario_por_rol(db, rol_id)