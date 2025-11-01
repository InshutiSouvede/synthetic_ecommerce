from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import controllers, schemas, database

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/", response_model=list[schemas.Customer])
def list_customers(db: Session = Depends(database.get_db)):
    return controllers.customers.get_customers(db)

@router.get("/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(database.get_db)):
    db_customer = controllers.customers.get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.post("/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(database.get_db)):
    return controllers.customers.create_customer(db, customer)

@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, customer: schemas.CustomerCreate, db: Session = Depends(database.get_db)):
    return controllers.customers.update_customer(db, customer_id, customer)

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(database.get_db)):
    return controllers.customers.delete_customer(db, customer_id)
