from sqlalchemy.orm import Session
from app.models.cita import Cita
from app.schemas.cita import CitaCreate

def crear_cita(db: Session, cita_data: CitaCreate) -> Cita:
    nueva_cita = Cita(**cita_data.model_dump())
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita

def obtener_cita_por_id(db: Session, cita_id: int) -> Cita | None:
    return db.query(Cita).filter(Cita.id == cita_id).first()

def obtener_citas(db: Session) -> list[Cita]:
    return db.query(Cita).all()

def eliminar_cita(db: Session, cita_id: int) -> Cita | None:
    cita = obtener_cita_por_id(db, cita_id)
    if cita:
        db.delete(cita)
        db.commit()
    return cita
