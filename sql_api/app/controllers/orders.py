from sqlalchemy.orm import Session
from app.models import Order
from app import schemas

def get_orders(db: Session):
    return db.query(Order).all()

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.order_id == order_id).first()

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: int, updated: schemas.OrderCreate):
    db_order = get_order(db, order_id)
    if db_order:
        for key, value in updated.dict().items():
            setattr(db_order, key, value)
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order
