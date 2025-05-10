from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship
from app.db.database import Base

class HorarioMedico(Base):
    __tablename__ = 'horarios_medicos'
    id = Column(Integer, primary_key=True)
    medico_id = Column(Integer, ForeignKey("medicos.id"))
    dia_semana = Column(String(20))
    hora_inicio = Column(Time)
    hora_fin = Column(Time)

    medico = relationship("Medico", back_populates="horarios")