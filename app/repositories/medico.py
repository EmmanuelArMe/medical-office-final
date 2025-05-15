from sqlalchemy.orm import Session
from app.models.medico import Medico
from app.schemas.medico import MedicoCreate, MedicoUpdate

def crear_medico(db: Session, medico: MedicoCreate) -> Medico:
    nuevo_medico = Medico(**medico.model_dump())
    db.add(nuevo_medico)
    db.commit()
    db.refresh(nuevo_medico)
    return nuevo_medico

def obtener_medico_por_documento(db: Session, medico_documento: int) -> Medico:
    return db.query(Medico).filter(Medico.documento == medico_documento).first()

def obtener_medicos(db: Session, skip: int, limit: int) -> list[Medico]:
    return db.query(Medico).offset(skip).limit(limit).all()

def eliminar_medico(db: Session, medico_documento: int) -> Medico:
    medico = obtener_medico_por_documento(db, medico_documento)
    if medico:
        db.delete(medico)
        db.commit()

def actualizar_medico(db: Session, medico: Medico, medico_data: MedicoUpdate) -> Medico | None:
    for key, value in medico_data.model_dump().items():
        setattr(medico, key, value)    
    db.commit()
    db.refresh(medico)
    return medico

def obtener_medicos_por_especialidad(db: Session, especialidad_id: int) -> list[Medico]:
    return db.query(Medico).filter(Medico.especialidad_id == especialidad_id).all()