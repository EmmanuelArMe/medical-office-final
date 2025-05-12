from fastapi import HTTPException, status
from app.models import Paciente, Medico, Consultorio
from app.models.cita import Cita
from app.schemas.cita import CitaCreate
from sqlalchemy.orm import Session
from app.repositories import cita as cita_repository
from sqlalchemy import extract

def crear_cita(db: Session, cita_data: CitaCreate):
    # Validar existencia del paciente
    paciente = db.query(Paciente).filter(Paciente.id == cita_data.paciente_id).first()
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un paciente con id {cita_data.paciente_id}"
        )

    # Validar existencia del médico
    medico = db.query(Medico).filter(Medico.id == cita_data.medico_id).first()
    if not medico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un médico con id {cita_data.medico_id}"
        )

    # Validar existencia del consultorio
    consultorio = db.query(Consultorio).filter(Consultorio.id == cita_data.consultorio_id).first()
    if not consultorio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un consultorio con id {cita_data.consultorio_id}"
        )
    
    # Validar la creación de una cita por paciente
    cita_existente = db.query(Cita).filter(
        Cita.paciente_id == cita_data.paciente_id,
        extract("year", Cita.fecha) == cita_data.fecha.year,
        extract("month", Cita.fecha) == cita_data.fecha.month,
        extract("day", Cita.fecha) == cita_data.fecha.day
    ).first()
    if cita_existente:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El paciente ya tiene una cita el mismo dia"
        )

    # Crear la cita
    nueva_cita = cita_repository.crear_cita(db, cita_data)
    if not nueva_cita:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear la cita"
        )
    return nueva_cita

def obtener_cita_por_id(db: Session, cita_id: int):
    # Validar existencia de la cita
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una cita con id {cita_id}"
        )
    return cita_repository.obtener_cita_por_id(db, cita_id)

def obtener_citas(db: Session, skip: int, limit: int):
    # Validar existencia de citas
    citas = db.query(Cita).all()
    if not citas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron citas"
        )
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a 0 y 1 respectivamente."
        )
    return cita_repository.obtener_citas(db, skip, limit)

def eliminar_cita(db: Session, cita_id: int):
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una cita con id {cita_id}"
        )

    cita_repository.eliminar_cita(db, cita_id)
    return cita


def actualizar_cita(db: Session, cita_id: int, cita_data: CitaCreate):
    cita = obtener_cita_por_id(db, cita_id)
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una cita con id {cita_id}"
        )
    
    # Validar existencia del paciente
    paciente = db.query(Paciente).filter(Paciente.id == cita_data.paciente_id).first()
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un paciente con id {cita_data.paciente_id}"
        )

    # Validar existencia del médico
    medico = db.query(Medico).filter(Medico.id == cita_data.medico_id).first()    
    if not medico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un médico con id {cita_data.medico_id}"
        )

    # Validar existencia del consultorio            
    consultorio = db.query(Consultorio).filter(Consultorio.id == cita_data.consultorio_id).first()
    if not consultorio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un consultorio con id {cita_data.consultorio_id}"
        )

    if cita:
        cita_actualizada = cita_repository.actualizar_cita(db, cita, cita_data)
        return cita_actualizada

def obtener_citas_por_paciente(db: Session, paciente_id: int):
    # Validar existencia del paciente
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un paciente con id {paciente_id}"
        )
    if not paciente.citas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron citas para el paciente con id {paciente_id}"
        )
    return cita_repository.obtener_citas_por_paciente(db, paciente_id)

def obtener_citas_por_medico(db: Session, medico_id: int):
    # Validar existencia del médico
    medico = db.query(Medico).filter(Medico.id == medico_id).first()
    if not medico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un médico con id {medico_id}"
        )
    if not medico.citas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron citas para el médico con id {medico_id}"
        )
    return cita_repository.obtener_citas_por_medico(db, medico_id)

def obtener_citas_por_consultorio(db: Session, consultorio_id: int):
    # Validar existencia del consultorio
    consultorio = db.query(Consultorio).filter(Consultorio.id == consultorio_id).first()
    if not consultorio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un consultorio con id {consultorio_id}"
        )
    if not consultorio.citas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron citas para el consultorio con id {consultorio_id}"
        )
    return cita_repository.obtener_citas_por_consultorio(db, consultorio_id)

def obtener_citas_por_fecha(db: Session, fecha: str):
    # Validar existencia de citas
    citas = db.query(Cita).filter(Cita.fecha == fecha).all()
    if not citas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron citas para la fecha {fecha}"
        )
    return cita_repository.obtener_citas_por_fecha(db, fecha)
