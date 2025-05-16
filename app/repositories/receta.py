from sqlalchemy.orm import Session
from app.models.receta import Receta
from app.schemas.receta import RecetaCreate, RecetaUpdate

def crear_receta(db: Session, receta: RecetaCreate) -> Receta:
    nueva_receta = Receta(**receta.model_dump())
    db.add(nueva_receta)
    db.commit()
    db.refresh(nueva_receta)
    return nueva_receta

def obtener_receta_por_id(db: Session, receta_id: int) -> Receta | None:
    return db.query(Receta).filter(Receta.id == receta_id).first()

def obtener_recetas(db: Session, skip: int, limit: int) -> list[Receta]:
    return db.query(Receta).offset(skip).limit(limit).all()

def eliminar_receta(db: Session, receta_id: int) -> Receta | None:
    receta = obtener_receta_por_id(db, receta_id)
    if receta:
        db.delete(receta)
        db.commit()

def actualizar_receta(db: Session, receta: Receta, receta_data: RecetaUpdate) -> Receta | None:
    for key, value in receta_data.model_dump().items():
        setattr(receta, key, value)
    db.commit()
    db.refresh(receta)
    return receta