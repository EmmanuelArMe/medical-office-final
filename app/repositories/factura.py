from sqlalchemy.orm import Session
from app.models.factura import Factura
from app.schemas.factura import FacturaCreate, FacturaUpdate

def crear_factura(db: Session, factura_data: FacturaCreate) -> Factura:
    nueva_factura = Factura(**factura_data.model_dump())
    db.add(nueva_factura)
    db.commit()
    db.refresh(nueva_factura)
    return nueva_factura

def obtener_factura_por_id(db: Session, factura_id: int) -> Factura | None:
    return db.query(Factura).filter(Factura.id == factura_id).first()

def obtener_facturas(db: Session, skip: int, limit: int) -> list[Factura]:
    return db.query(Factura).offset(skip).limit(limit).all()

def eliminar_factura(db: Session, factura_id: int) -> Factura | None:
    factura = obtener_factura_por_id(db, factura_id)
    if factura:
        db.delete(factura)
        db.commit()

def actualizar_factura(db: Session, factura: Factura, factura_data: FacturaUpdate) -> Factura | None:
    for key, value in factura_data.model_dump().items():
        setattr(factura, key, value)
    db.commit()
    db.refresh(factura)
    return factura

def obtener_factura_por_pago_id(db: Session, pago_id: int) -> Factura | None:
    return db.query(Factura).filter(Factura.pago_id == pago_id).first()