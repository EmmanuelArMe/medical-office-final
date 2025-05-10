from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Receta(Base):
    __tablename__ = 'recetas'
    id = Column(Integer, primary_key=True)
    cita_id = Column(Integer, ForeignKey("citas.id"))
    instrucciones = Column(Text)

    cita = relationship("Cita", back_populates="receta")
    medicamentos = relationship("MedicamentoRecetado", back_populates="receta")