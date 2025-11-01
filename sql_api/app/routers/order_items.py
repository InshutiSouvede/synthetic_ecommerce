from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import controllers, schemas, database

router = APIRouter(prefix="/order-items", tags=["Order Items"])

@router.get("/", response_model=list[schemas.OrderItem])
def list_order_items(db: Session = Depends(database.get_db)):
    return controllers.order_items.get_order_items(db)

@router.get("/{order_item_id}", response_model=schemas.OrderItem)
def read_order_item(order_item_id: int, db: Session = Depends(database.get_db)):
    db_item = controllers.order_items.get_order_item(db, order_item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return db_item

@router.post("/", response_model=schemas.OrderItem)
def create_order_item(order_item: schemas.OrderItemCreate, db: Session = Depends(database.get_db)):
    return controllers.order_items.create_order_item(db, order_item)

@router.put("/{order_item_id}", response_model=schemas.OrderItem)
def update_order_item(order_item_id: int, order_item: schemas.OrderItemCreate, db: Session = Depends(database.get_db)):
    return controllers.order_items.update_order_item(db, order_item_id, order_item)

@router.delete("/{order_item_id}")
def delete_order_item(order_item_id: int, db: Session = Depends(database.get_db)):
    return controllers.order_items.delete_order_item(db, order_item_id)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import controllers, schemas, database

router = APIRouter(prefix="/order-items", tags=["Order Items"])

@router.get("/", response_model=list[schemas.OrderItem])
def list_order_items(db: Session = Depends(database.get_db)):
    return controllers.order_items.get_order_items(db)

@router.get("/{order_item_id}", response_model=schemas.OrderItem)
def read_order_item(order_item_id: int, db: Session = Depends(database.get_db)):
    db_item = controllers.order_items.get_order_item(db, order_item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return db_item

@router.post("/", response_model=schemas.OrderItem)
def create_order_item(order_item: schemas.OrderItemCreate, db: Session = Depends(database.get_db)):
    return controllers.order_items.create_order_item(db, order_item)

@router.put("/{order_item_id}", response_model=schemas.OrderItem)
def update_order_item(order_item_id: int, order_item: schemas.OrderItemCreate, db: Session = Depends(database.get_db)):
    return controllers.order_items.update_order_item(db, order_item_id, order_item)

@router.delete("/{order_item_id}")
def delete_order_item(order_item_id: int, db: Session = Depends(database.get_db)):
    return controllers.order_items.delete_order_item(db, order_item_id)
