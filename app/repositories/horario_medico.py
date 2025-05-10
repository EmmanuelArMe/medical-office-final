from sqlalchemy.orm import Session
from app.models.horario_medico import HorarioMedico

def crear_horario_medico(db: Session, horario: HorarioMedico) -> HorarioMedico:
    db.add(horario)
    db.commit()
    db.refresh(horario)
    return horario

def obtener_horarios(db: Session):
    return db.query(HorarioMedico).all()

def obtener_horario_por_id(db: Session, id: int):
    return db.query(HorarioMedico).filter(HorarioMedico.id == id).first()

def actualizar_horario_medico(db: Session, id: int, data: dict):
    horario = obtener_horario_por_id(db, id)
    if horario:
        for key, value in data.items():
            setattr(horario, key, value)
        db.commit()
        db.refresh(horario)
    return horario

def eliminar_horario_medico(db: Session, id: int):
    horario = obtener_horario_por_id(db, id)
    if horario:
        db.delete(horario)
        db.commit()
    return horario
