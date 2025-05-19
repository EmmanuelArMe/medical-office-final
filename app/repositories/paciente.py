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
    pacientes = db.query(Paciente).offset(skip).limit(limit).all()
    # Transformar las instancias en diccionarios con datos desencriptados
    resultado = []
    
    for paciente in pacientes:
        try:
            resultado.append({
                "id": paciente.id,
                "nombre": paciente.nombre,
                "apellido": paciente.apellido,
                "fecha_nacimiento": paciente.fecha_nacimiento,
                "documento": paciente.documento,
                "telefono": paciente.telefono,    # Esto usa el property getter
                "email": paciente.email,          # Esto usa el property getter
            })
        except Exception as e:
            # Si hay error en la desencriptación de algún campo, incluimos el paciente
            # con los campos problemáticos marcados como [ERROR DE ENCRIPTACIÓN]
            resultado.append({
                "id": paciente.id,
                "nombre": paciente.nombre,
                "apellido": paciente.apellido,
                "fecha_nacimiento": paciente.fecha_nacimiento,
                "documento": paciente.documento,
                "telefono": "[ERROR DE ENCRIPTACIÓN]" if paciente._telefono else None,
                "email": "[ERROR DE ENCRIPTACIÓN]" if paciente._email else None,
            })
    
    return resultado

def eliminar_paciente(db: Session, documento: str):
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
