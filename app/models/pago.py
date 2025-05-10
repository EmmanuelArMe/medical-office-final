from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from app.db.database import Base

class Pago(Base):
    __tablename__ = 'pagos'
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    monto = Column(Float)
    fecha = Column(DateTime)
    metodo_pago = Column(String(50))