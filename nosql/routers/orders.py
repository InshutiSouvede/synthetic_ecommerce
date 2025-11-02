from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import get_database
from models import Order, OrderCreate, OrderUpdate
from services import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])

def get_order_service(database: AsyncIOMotorDatabase = Depends(get_database)) -> OrderService:
    return OrderService(database)

@router.post("/", response_model=Order)
async def create_order(
    order: OrderCreate,
    service: OrderService = Depends(get_order_service)
):
    """Create a new order"""
    return await service.create_order(order)

@router.get("/", response_model=List[Order])
async def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: OrderService = Depends(get_order_service)
):
    """Get all orders with pagination"""
    return await service.get_orders(skip=skip, limit=limit)

@router.get("/customer/{customer_id}", response_model=List[Order])
async def get_orders_by_customer(
    customer_id: int,
    service: OrderService = Depends(get_order_service)
):
    """Get orders by customer ID"""
    return await service.get_orders_by_customer(customer_id)

@router.get("/{order_id}", response_model=Order)
async def get_order(
    order_id: str,
    service: OrderService = Depends(get_order_service)
):
    """Get an order by MongoDB ObjectId"""
    order = await service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/by-order-id/{order_id}", response_model=Order)
async def get_order_by_order_id(
    order_id: int,
    service: OrderService = Depends(get_order_service)
):
    """Get an order by their order_id"""
    order = await service.get_order_by_order_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{order_id}", response_model=Order)
async def update_order(
    order_id: str,
    order_update: OrderUpdate,
    service: OrderService = Depends(get_order_service)
):
    """Update an order"""
    order = await service.update_order(order_id, order_update)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.delete("/{order_id}")
async def delete_order(
    order_id: str,
    service: OrderService = Depends(get_order_service)
):
    """Delete an order"""
    success = await service.delete_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}