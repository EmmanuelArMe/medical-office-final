from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Medicamento(Base):
    __tablename__ = 'medicamentos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)

    recetas = relationship("MedicamentoRecetado", back_populates="medicamento")