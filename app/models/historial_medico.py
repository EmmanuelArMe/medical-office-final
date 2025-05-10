from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class HistorialMedico(Base):
    __tablename__ = 'historial_medico'
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    descripcion = Column(Text)
    fecha = Column(DateTime)

    paciente = relationship("Paciente", back_populates="historial_medico")