from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.repositories import usuario as usuario_repository

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
    nuevo_usuario = usuario_repository.crear_usuario(db, usuario)
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
    usuario = obtener_usuario_por_id(db, usuario_id)
    usuario_actualizado = usuario_repository.actualizar_usuario(db, usuario, usuario_data)
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