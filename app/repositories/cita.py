from sqlalchemy.orm import Session
from app.models.cita import Cita
from app.schemas.cita import CitaCreate, CitaUpdate

def crear_cita(db: Session, cita_data: CitaCreate) -> Cita:
    nueva_cita = Cita(**cita_data.model_dump())
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita

def obtener_cita_por_id(db: Session, cita_id: int) -> Cita | None:
    return db.query(Cita).filter(Cita.id == cita_id).first()

def obtener_citas(db: Session, skip: int, limit: int) -> list[Cita]:
    return db.query(Cita).offset(skip).limit(limit).all()

def eliminar_cita(db: Session, cita_id: int) -> None:
    cita = obtener_cita_por_id(db, cita_id)
    if cita:
        db.delete(cita)
        db.commit()


def actualizar_cita(db: Session, cita: Cita, cita_data: CitaUpdate) -> Cita | None:
    for key, value in cita_data.model_dump().items():
        setattr(cita, key, value)
    db.commit()
    db.refresh(cita)
    return cita

def obtener_citas_por_paciente(db: Session, paciente_id: int) -> list[Cita]:
    return db.query(Cita).filter(Cita.paciente_id == paciente_id).all()

def obtener_citas_por_medico(db: Session, medico_id: int) -> list[Cita]:
    return db.query(Cita).filter(Cita.medico_id == medico_id).all()

def obtener_citas_por_consultorio(db: Session, consultorio_id: int) -> list[Cita]:
    return db.query(Cita).filter(Cita.consultorio_id == consultorio_id).all()

def obtener_citas_por_fecha(db: Session, fecha: str) -> list[Cita]:
    return db.query(Cita).filter(Cita.fecha == fecha).all()
