from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Medico(Base):
    __tablename__ = 'medicos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    especialidad_id = Column(Integer, ForeignKey("especialidades.id"))
    email = Column(String(100))
    telefono = Column(String(20))

    especialidad = relationship("Especialidad", back_populates="medicos")
    citas = relationship("Cita", back_populates="medico")
    horarios = relationship("HorarioMedico", back_populates="medico")