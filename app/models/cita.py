from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Cita(Base):
    __tablename__ = 'citas'
    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, nullable=False)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    medico_id = Column(Integer, ForeignKey("medicos.id"))
    consultorio_id = Column(Integer, ForeignKey("consultorios.id"))
    motivo = Column(Text)

    paciente = relationship("Paciente", back_populates="citas")
    medico = relationship("Medico", back_populates="citas")
    consultorio = relationship("Consultorio", back_populates="citas")
    receta = relationship("Receta", back_populates="cita", uselist=False)
    diagnostico = relationship("Diagnostico", back_populates="cita", uselist=False)