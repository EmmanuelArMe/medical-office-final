from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Rol(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)

    usuarios = relationship("Usuario", back_populates="rol")