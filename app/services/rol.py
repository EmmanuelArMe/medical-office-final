from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.rol import Rol
from app.schemas.rol import RolCreate, RolUpdate
from app.repositories import rol as rol_repository

def crear_rol(db: Session, rol: RolCreate):
    rol_existente = db.query(Rol).filter(Rol.nombre == rol.nombre).first()
    if rol_existente:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un rol con el nombre '{rol.nombre}'"
        )
    nuevo_rol = rol_repository.crear_rol(db, rol)
    if not nuevo_rol:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el rol"
        )
    return nuevo_rol

def obtener_rol_por_id(db: Session, rol_id: int):
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El rol con ID {rol_id} no fue encontrado."
        )
    return rol_repository.obtener_rol_por_id(db, rol_id)

def obtener_roles(db: Session):
    roles = db.query(Rol).all()
    if not roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron roles."
        )
    return rol_repository.obtener_roles(db)

def actualizar_rol(db: Session, rol_id: int, rol_data: RolUpdate):
    rol = obtener_rol_por_id(db, rol_id)
    rol_actualizado = rol_repository.actualizar_rol(db, rol, rol_data)
    if not rol_actualizado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el rol"
        )
    return rol_actualizado

def eliminar_rol(db: Session, rol_id: int):
    rol = obtener_rol_por_id(db, rol_id)
    rol_repository.eliminar_rol(db, rol_id)
    return rol