from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from app.db.database import Base

class Factura(Base):
    __tablename__ = 'facturas'
    id = Column(Integer, primary_key=True)
    pago_id = Column(Integer, ForeignKey("pagos.id"))
    detalle = Column(Text)
    fecha_emision = Column(DateTime)