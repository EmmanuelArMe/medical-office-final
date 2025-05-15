from sqlalchemy.orm import Session
from app.models.paciente import Paciente
from app.schemas.paciente import PacienteCreate, PacienteUpdate

def crear_paciente(db: Session, paciente: PacienteCreate):
    nuevo_paciente = Paciente(**paciente.model_dump())
    db.add(nuevo_paciente)
    db.commit()
    db.refresh(nuevo_paciente)
    return nuevo_paciente

def obtener_paciente_por_documento(db: Session, documento: int):
    return db.query(Paciente).filter(Paciente.documento == documento).first()

def obtener_pacientes(db: Session, skip: int, limit: int):
    return db.query(Paciente).offset(skip).limit(limit).all()

def eliminar_paciente(db: Session, documento: int):
    paciente = obtener_paciente_por_documento(db, documento)
    if paciente:
        db.delete(paciente)
        db.commit()

def actualizar_paciente(db: Session, paciente: Paciente, paciente_data: PacienteUpdate) -> Paciente | None:
    for key, value in paciente_data.model_dump().items():
        setattr(paciente, key, value)
    db.commit()
    db.refresh(paciente)
    return paciente
