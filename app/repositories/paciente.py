from sqlalchemy.orm import Session
from app.models.paciente import Paciente
from app.schemas.paciente import PacienteCreate

def crear_paciente(db: Session, paciente: PacienteCreate):
    db_paciente = Paciente(**paciente.model_dump())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

def obtener_pacientes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Paciente).offset(skip).limit(limit).all()

def obtener_paciente(db: Session, documento: int):
    return db.query(Paciente).filter(Paciente.documento == documento).first()

def eliminar_paciente(db: Session, documento: int):
    paciente = db.query(Paciente).filter(Paciente.documento == documento).first()
    if paciente:
        db.delete(paciente)
        db.commit()

def actualizar_paciente(db: Session, paciente: Paciente, paciente_data: PacienteCreate) -> Paciente | None:
    for key, value in paciente_data.model_dump().items():
        setattr(paciente, key, value)
    db.commit()
    db.refresh(paciente)
    return paciente
