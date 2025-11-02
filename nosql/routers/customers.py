from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import get_database
from models import Customer, CustomerCreate, CustomerUpdate
from services import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])

def get_customer_service(database: AsyncIOMotorDatabase = Depends(get_database)) -> CustomerService:
    return CustomerService(database)

@router.post("/", response_model=Customer)
async def create_customer(
    customer: CustomerCreate,
    service: CustomerService = Depends(get_customer_service)
):
    """Create a new customer"""
    return await service.create_customer(customer)

@router.get("/", response_model=List[Customer])
async def get_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: CustomerService = Depends(get_customer_service)
):
    """Get all customers with pagination"""
    return await service.get_customers(skip=skip, limit=limit)

@router.get("/{customer_id}", response_model=Customer)
async def get_customer(
    customer_id: str,
    service: CustomerService = Depends(get_customer_service)
):
    """Get a customer by MongoDB ObjectId"""
    customer = await service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.get("/by-customer-id/{customer_id}", response_model=Customer)
async def get_customer_by_customer_id(
    customer_id: int,
    service: CustomerService = Depends(get_customer_service)
):
    """Get a customer by their customer_id"""
    customer = await service.get_customer_by_customer_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=Customer)
async def update_customer(
    customer_id: str,
    customer_update: CustomerUpdate,
    service: CustomerService = Depends(get_customer_service)
):
    """Update a customer"""
    customer = await service.update_customer(customer_id, customer_update)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.delete("/{customer_id}")
async def delete_customer(
    customer_id: str,
    service: CustomerService = Depends(get_customer_service)
):
    """Delete a customer"""
    success = await service.delete_customer(customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}