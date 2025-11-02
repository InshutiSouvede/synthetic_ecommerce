from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.controllers import orders as orders_controller
from app import schemas
from app.database import get_db
router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=list[schemas.Order])
def list_orders(db: Session = Depends(get_db)):
    return orders_controller.get_orders(db)

@router.get("/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = orders_controller.get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return orders_controller.create_order(db, order)

@router.put("/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return orders_controller.update_order(db, order_id, order)

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return orders_controller.delete_order(db, order_id)
