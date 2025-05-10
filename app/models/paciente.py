from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.db.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    documento = Column(String(50), unique=True, nullable=False)
    telefono = Column(String(20))
    email = Column(String(100))

    citas = relationship("Cita", back_populates="paciente")
    historial_medico = relationship("HistorialMedico", back_populates="paciente")
