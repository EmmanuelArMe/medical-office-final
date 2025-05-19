from sqlalchemy.orm import Session
from app.models.medico import Medico
from app.schemas.medico import MedicoCreate, MedicoUpdate

def crear_medico(db: Session, medico: MedicoCreate) -> Medico:
    nuevo_medico = Medico(**medico.model_dump())
    db.add(nuevo_medico)
    db.commit()
    db.refresh(nuevo_medico)
    return nuevo_medico

def obtener_medico_por_documento(db: Session, documento: str) -> Medico:
    return db.query(Medico).filter(Medico.documento == documento).first()

def obtener_medicos(db: Session, skip: int, limit: int) -> list[Medico]:
    medicos = db.query(Medico).offset(skip).limit(limit).all()
    # Transformar las instancias en diccionarios con datos desencriptados
    resultado = []
    for medico in medicos:
        try:
            resultado.append({
                "id": medico.id,
                "nombre": medico.nombre,
                "apellido": medico.apellido,
                "especialidad_id": medico.especialidad_id,
                "documento": medico.documento,
                "email": medico.email,          # Esto usa el property getter
                "telefono": medico.telefono,    # Esto usa el property getter
            })
        except Exception as e:
            # Si hay error en la desencriptación de algún campo, incluimos el paciente
            # con los campos problemáticos marcados como [ERROR DE ENCRIPTACIÓN]
            resultado.append({
                "id": medico.id,
                "nombre": medico.nombre,
                "apellido": medico.apellido,
                "especialidad_id": medico.especialidad_id,
                "documento": medico.documento,
                "telefono": "[ERROR DE ENCRIPTACIÓN]" if medico._telefono else None,
                "email": "[ERROR DE ENCRIPTACIÓN]" if medico._email else None,
            })
    return resultado

def eliminar_medico(db: Session, documento: str) -> Medico:
    medico = obtener_medico_por_documento(db, documento)
    if medico:
        db.delete(medico)
        db.commit()

def actualizar_medico(db: Session, medico: Medico, medico_data: MedicoUpdate) -> Medico | None:
    for key, value in medico_data.model_dump().items():
        setattr(medico, key, value)    
    db.commit()
    db.refresh(medico)
    return medico

def obtener_medicos_por_especialidad(db: Session, especialidad_id: int) -> list[Medico]:
    return db.query(Medico).filter(Medico.especialidad_id == especialidad_id).all()