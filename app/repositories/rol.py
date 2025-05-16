from sqlalchemy.orm import Session
from app.models.rol import Rol
from app.schemas.rol import RolCreate, RolUpdate

def crear_rol(db: Session, rol_data: RolCreate) -> Rol:
    nuevo_rol = Rol(**rol_data.model_dump())
    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)
    return nuevo_rol

def obtener_rol_por_id(db: Session, rol_id: int) -> Rol | None:
    return db.query(Rol).filter(Rol.id == rol_id).first()

def obtener_roles(db: Session, skip: int, limit: int) -> list[Rol]:
    return db.query(Rol).offset(skip).limit(limit).all()

def eliminar_rol(db: Session, rol_id: int) -> Rol | None:
    rol = obtener_rol_por_id(db, rol_id)
    if rol:
        db.delete(rol)
        db.commit()

def actualizar_rol(db: Session, rol: Rol, rol_data: RolUpdate) -> Rol | None:
    for key, value in rol_data.model_dump().items():
        setattr(rol, key, value)
    db.commit()
    db.refresh(rol)
    return rol
