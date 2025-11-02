from sqlalchemy.orm import Session
from app.models import OrderItem
from app import schemas

def get_order_items(db: Session):
    return db.query(OrderItem).all()

def get_order_item(db: Session, order_item_id: int):
    return db.query(OrderItem).filter(OrderItem.order_item_id == order_item_id).first()

def create_order_item(db: Session, order_item: schemas.OrderItemCreate):
    db_item = OrderItem(**order_item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_order_item(db: Session, order_item_id: int, updated: schemas.OrderItemCreate):
    db_item = get_order_item(db, order_item_id)
    if db_item:
        for key, value in updated.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_order_item(db: Session, order_item_id: int):
    db_item = get_order_item(db, order_item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
