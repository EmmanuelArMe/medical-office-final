from sqlalchemy.orm import Session
from app.models.consultorio import Consultorio
from app.schemas.consultorio import ConsultorioCreate, ConsultorioUpdate

def crear_consultorio(db: Session, consultorio_data: ConsultorioCreate) -> Consultorio:
    nuevo_consultorio = Consultorio(**consultorio_data.model_dump())
    db.add(nuevo_consultorio)
    db.commit()
    db.refresh(nuevo_consultorio)
    return nuevo_consultorio

def obtener_consultorio_por_id(db: Session, consultorio_id: int) -> Consultorio | None:
    return db.query(Consultorio).filter(Consultorio.id == consultorio_id).first()

def obtener_consultorios(db: Session, skip: int, limit: int) -> list[Consultorio]:
    return db.query(Consultorio).offset(skip).limit(limit).all()

def eliminar_consultorio(db: Session, consultorio_id: int) -> Consultorio | None:
    consultorio = obtener_consultorio_por_id(db, consultorio_id)
    if consultorio:
        db.delete(consultorio)
        db.commit()

def actualizar_consultorio(db: Session, consultorio: Consultorio, consultorio_data: ConsultorioUpdate) -> Consultorio | None:
    for key, value in consultorio_data.model_dump().items():
        setattr(consultorio, key, value)
    db.commit()
    db.refresh(consultorio)
    return consultorio
