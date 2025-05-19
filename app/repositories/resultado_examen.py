from sqlalchemy.orm import Session
from app.models.resultado_examen import ResultadoExamen
from app.schemas.resultado_examen import ResultadoExamenCreate, ResultadoExamenUpdate

def crear_resultado_examen(db: Session, resultado_examen: ResultadoExamenCreate) -> ResultadoExamen:
    nuevo_resultado_examen = ResultadoExamen(**resultado_examen.model_dump())
    db.add(nuevo_resultado_examen)
    db.commit()
    db.refresh(nuevo_resultado_examen)
    return nuevo_resultado_examen

def obtener_resultado_examen_por_id(db: Session, resultado_examen_id: int) -> ResultadoExamen | None:
    return db.query(ResultadoExamen).filter(ResultadoExamen.id == resultado_examen_id).first()

def obtener_resultado_examen(db: Session, skip: int, limit: int) -> list[ResultadoExamen]:
    return db.query(ResultadoExamen).offset(skip).limit(limit).all()

def eliminar_resultado_examen(db: Session, resultado_examen_id: int) -> ResultadoExamen | None:
    resultado_examen = obtener_resultado_examen_por_id(db, resultado_examen_id)
    if resultado_examen:
        db.delete(resultado_examen)
        db.commit()

def actualizar_resultado_examen(db: Session, resultado_examen: ResultadoExamen, resultado_examen_data: ResultadoExamenUpdate) -> ResultadoExamen | None:
    for key, value in resultado_examen_data.model_dump().items():
        setattr(resultado_examen, key, value)
    db.commit()
    db.refresh(resultado_examen)
    return resultado_examen

def obtener_resultado_examen_por_paciente_id(db: Session, paciente_id: int) -> ResultadoExamen | None:
    return db.query(ResultadoExamen).filter(ResultadoExamen.paciente_id == paciente_id).first()