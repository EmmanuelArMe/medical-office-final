from sqlalchemy.orm import Session
from app.models.medicamento_recetado import MedicamentoRecetado
from app.schemas.medicamento_recetado import MedicamentoRecetadoCreate, MedicamentoRecetadoUpdate

def crear_medicamento_recetado(db: Session, medicamento_recetado_data: MedicamentoRecetadoCreate) -> MedicamentoRecetado:
    nuevo_medicamento_recetado = MedicamentoRecetado(**medicamento_recetado_data.model_dump())
    db.add(nuevo_medicamento_recetado)
    db.commit()
    db.refresh(nuevo_medicamento_recetado)
    return nuevo_medicamento_recetado

def obtener_medicamento_recetado_por_id(db: Session, medicamento_recetado_id: int) -> MedicamentoRecetado | None:
    return db.query(MedicamentoRecetado).filter(MedicamentoRecetado.id == medicamento_recetado_id).first()

def obtener_medicamentos_recetados(db: Session, skip: int, limit: int) -> list[MedicamentoRecetado]:
    return db.query(MedicamentoRecetado).offset(skip).limit(limit).all()

def eliminar_medicamento_recetado(db: Session, medicamento_recetado_id: int) -> MedicamentoRecetado | None:
    medicamento_recetado = obtener_medicamento_recetado_por_id(db, medicamento_recetado_id)
    if medicamento_recetado:
        db.delete(medicamento_recetado)
        db.commit()
    return medicamento_recetado

def actualizar_medicamento_recetado(db: Session, medicamento_recetado: MedicamentoRecetado, medicamento_recetado_data: MedicamentoRecetadoUpdate) -> MedicamentoRecetado | None:
    for key, value in medicamento_recetado_data.model_dump().items():
        setattr(medicamento_recetado, key, value)
    db.commit()
    db.refresh(medicamento_recetado)
    return medicamento_recetado

def obtener_medicamentos_recetados_por_receta(db: Session, receta_id: int) -> list[MedicamentoRecetado]:
    return db.query(MedicamentoRecetado).filter(MedicamentoRecetado.receta_id == receta_id).all()

def obtener_medicamentos_recetados_por_medicamento(db: Session, medicamento_id: int) -> list[MedicamentoRecetado]:
    return db.query(MedicamentoRecetado).filter(MedicamentoRecetado.medicamento_id == medicamento_id).all()