from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Consultorio(Base):
    __tablename__ = 'consultorios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    piso = Column(Integer)

    citas = relationship("Cita", back_populates="consultorio")