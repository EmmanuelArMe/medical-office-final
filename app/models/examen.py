from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class Examen(Base):
    __tablename__ = 'examenes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    descripcion = Column(Text)