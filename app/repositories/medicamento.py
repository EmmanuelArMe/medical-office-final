from sqlalchemy.orm import Session
from app.models.medicamento import Medicamento
from app.schemas.medicamento import MedicamentoCreate, MedicamentoUpdate

def crear_medicamento(db: Session, medicamento_data: MedicamentoCreate) -> Medicamento:
    nuevo_medicamento = Medicamento(**medicamento_data.model_dump())
    db.add(nuevo_medicamento)
    db.commit()
    db.refresh(nuevo_medicamento)
    return nuevo_medicamento

def obtener_medicamento_por_id(db: Session, medicamento_id: int) -> Medicamento | None:
    return db.query(Medicamento).filter(Medicamento.id == medicamento_id).first()

def obtener_medicamentos(db: Session, skip: int, limit: int) -> list[Medicamento]:
    return db.query(Medicamento).offset(skip).limit(limit).all()

def eliminar_medicamento(db: Session, medicamento_id: int) -> Medicamento | None:
    medicamento = obtener_medicamento_por_id(db, medicamento_id)
    if medicamento:
        db.delete(medicamento)
        db.commit()

def actualizar_medicamento(db: Session, medicamento: Medicamento, medicamento_data: MedicamentoUpdate) -> Medicamento | None:
    for key, value in medicamento_data.model_dump().items():
        setattr(medicamento, key, value)
    db.commit()
    db.refresh(medicamento)
    return medicamento