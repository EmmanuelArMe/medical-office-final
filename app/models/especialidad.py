from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Especialidad(Base):
    __tablename__ = 'especialidades'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)

    medicos = relationship("Medico", back_populates="especialidad")