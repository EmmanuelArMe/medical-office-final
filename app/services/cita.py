from fastapi import HTTPException, status
from app.models import Paciente, Medico, Consultorio
from app.models.cita import Cita
from app.schemas.cita import CitaCreate
from sqlalchemy.orm import Session

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

    # Crear la cita
    nueva_cita = Cita(**cita_data.model_dump())
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita

