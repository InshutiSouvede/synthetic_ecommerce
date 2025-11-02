from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.controllers import order_items as order_items_controller
from app import schemas
from app.database import get_db
router = APIRouter(prefix="/order-items", tags=["Order Items"])

@router.get("/", response_model=list[schemas.OrderItem])
def list_order_items(db: Session = Depends(get_db)):
    return order_items_controller.get_order_items(db)

@router.get("/{order_item_id}", response_model=schemas.OrderItem)
def read_order_item(order_item_id: int, db: Session = Depends(get_db)):
    db_item = order_items_controller.get_order_item(db, order_item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return db_item

@router.post("/", response_model=schemas.OrderItem)
def create_order_item(order_item: schemas.OrderItemCreate, db: Session = Depends(get_db)):
    return order_items_controller.create_order_item(db, order_item)

@router.put("/{order_item_id}", response_model=schemas.OrderItem)
def update_order_item(order_item_id: int, order_item: schemas.OrderItemCreate, db: Session = Depends(get_db)):
    return order_items_controller.update_order_item(db, order_item_id, order_item)

@router.delete("/{order_item_id}")
def delete_order_item(order_item_id: int, db: Session = Depends(get_db)):
    return order_items_controller.delete_order_item(db, order_item_id)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import controllers, schemas, database

router = APIRouter(prefix="/order-items", tags=["Order Items"])

@router.get("/", response_model=list[schemas.OrderItem])
def list_order_items(db: Session = Depends(get_db)):
    return order_items_controller.get_order_items(db)

@router.get("/{order_item_id}", response_model=schemas.OrderItem)
def read_order_item(order_item_id: int, db: Session = Depends(get_db)):
    db_item = order_items_controller.get_order_item(db, order_item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return db_item

@router.post("/", response_model=schemas.OrderItem)
def create_order_item(order_item: schemas.OrderItemCreate, db: Session = Depends(get_db)):
    return order_items_controller.create_order_item(db, order_item)

@router.put("/{order_item_id}", response_model=schemas.OrderItem)
def update_order_item(order_item_id: int, order_item: schemas.OrderItemCreate, db: Session = Depends(get_db)):
    return order_items_controller.update_order_item(db, order_item_id, order_item)

@router.delete("/{order_item_id}")
def delete_order_item(order_item_id: int, db: Session = Depends(get_db)):
    return order_items_controller.delete_order_item(db, order_item_id)
