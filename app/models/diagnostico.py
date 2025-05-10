from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Diagnostico(Base):
    __tablename__ = 'diagnosticos'
    id = Column(Integer, primary_key=True)
    cita_id = Column(Integer, ForeignKey("citas.id"))
    descripcion = Column(Text)

    cita = relationship("Cita", back_populates="diagnostico")