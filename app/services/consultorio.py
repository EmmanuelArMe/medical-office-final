from sqlalchemy.orm import Session
from app.models.consultorio import Consultorio
from app.schemas.consultorio import ConsultorioCreate
from app.repositories import consultorio as consultorio_repository

def crear_consultorio(db: Session, data: ConsultorioCreate):
    consultorio = Consultorio(**data.model_dump())
    return consultorio_repository.crear_consultorio(db, consultorio)

def listar_consultorios(db: Session):
    return consultorio_repository.obtener_todos_consultorios(db)

def obtener_consultorio(db: Session, consultorio_id: int):
    return consultorio_repository.obtener_consultorio_por_id(db, consultorio_id)

def eliminar_consultorio(db: Session, consultorio_id: int):
    return consultorio_repository.eliminar_consultorio(db, consultorio_id)