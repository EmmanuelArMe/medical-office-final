from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class MedicamentoRecetado(Base):
    __tablename__ = 'medicamento_recetado'
    id = Column(Integer, primary_key=True)
    receta_id = Column(Integer, ForeignKey("recetas.id"))
    medicamento_id = Column(Integer, ForeignKey("medicamentos.id"))
    dosis = Column(String(100))

    receta = relationship("Receta", back_populates="medicamentos")
    medicamento = relationship("Medicamento", back_populates="recetas")