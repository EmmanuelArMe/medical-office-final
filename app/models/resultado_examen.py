from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from app.db.database import Base

class ResultadoExamen(Base):
    __tablename__ = 'resultados_examenes'
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    examen_id = Column(Integer, ForeignKey("examenes.id"))
    resultado = Column(Text)
    fecha_realizacion = Column(DateTime)