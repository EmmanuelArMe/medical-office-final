from sqlalchemy.orm import Session
from app.models.consultorio import Consultorio

def crear_consultorio(db: Session, consultorio: str):
    db.add(consultorio)
    db.commit()
    db.refresh(consultorio)
    return consultorio

def obtener_todos_consultorios(db: Session):
    return db.query(Consultorio).all()

def obtener_consultorio_por_id(db: Session, consultorio_id: int):
    return db.query(Consultorio).filter(Consultorio.id == consultorio_id).first()

def eliminar_consultorio(db: Session, consultorio_id: int):
    consultorio = obtener_consultorio_por_id(db, consultorio_id)
    if consultorio:
        db.delete(consultorio)
        db.commit()
        return consultorio
    return None