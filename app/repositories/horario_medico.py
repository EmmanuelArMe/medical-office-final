from sqlalchemy.orm import Session
from app.models.horario_medico import HorarioMedico
from app.schemas.horario_medico import HorarioMedicoCreate, HorarioMedicoUpdate

def crear_horario_medico(db: Session, horario: HorarioMedico):
    nuevo_horario = HorarioMedico(**horario.model_dump())
    db.add(nuevo_horario)
    db.commit()
    db.refresh(nuevo_horario)
    return nuevo_horario

def obtener_horario_medico_por_id(db: Session, id: int):
    return db.query(HorarioMedico).filter(HorarioMedico.id == id).first()

def obtener_horarios_medicos(db: Session, skip: int, limit: int):
    return db.query(HorarioMedico).offset(skip).limit(limit).all()

def eliminar_horario_medico(db: Session, id: int):
    horario_medico = obtener_horario_medico_por_id(db, id)
    if horario_medico:
        db.delete(horario_medico)
        db.commit()

def actualizar_horario_medico(db: Session, horario_medico: HorarioMedico, horario_medico_data: HorarioMedicoUpdate) -> HorarioMedico | None:
    for key, value in horario_medico_data.model_dump().items():
        setattr(horario_medico, key, value)
    db.commit()
    db.refresh(horario_medico)
    return horario_medico

def obtener_horarios_medicos_por_id_medico(db: Session, medico_id: int):
    return db.query(HorarioMedico).filter(HorarioMedico.medico_id == medico_id).all()