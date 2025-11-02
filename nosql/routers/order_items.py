from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import get_database
from models import OrderItem, OrderItemCreate, OrderItemUpdate
from services import OrderItemService

router = APIRouter(prefix="/order-items", tags=["order-items"])

def get_order_item_service(database: AsyncIOMotorDatabase = Depends(get_database)) -> OrderItemService:
    return OrderItemService(database)

@router.post("/", response_model=OrderItem)
async def create_order_item(
    order_item: OrderItemCreate,
    service: OrderItemService = Depends(get_order_item_service)
):
    """Create a new order item"""
    return await service.create_order_item(order_item)

@router.get("/", response_model=List[OrderItem])
async def get_order_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: OrderItemService = Depends(get_order_item_service)
):
    """Get all order items with pagination"""
    return await service.get_order_items(skip=skip, limit=limit)

@router.get("/order/{order_id}", response_model=List[OrderItem])
async def get_order_items_by_order(
    order_id: int,
    service: OrderItemService = Depends(get_order_item_service)
):
    """Get order items by order ID"""
    return await service.get_order_items_by_order(order_id)

@router.get("/{order_item_id}", response_model=OrderItem)
async def get_order_item(
    order_item_id: str,
    service: OrderItemService = Depends(get_order_item_service)
):
    """Get an order item by MongoDB ObjectId"""
    order_item = await service.get_order_item(order_item_id)
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return order_item

@router.put("/{order_item_id}", response_model=OrderItem)
async def update_order_item(
    order_item_id: str,
    order_item_update: OrderItemUpdate,
    service: OrderItemService = Depends(get_order_item_service)
):
    """Update an order item"""
    order_item = await service.update_order_item(order_item_id, order_item_update)
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return order_item

@router.delete("/{order_item_id}")
async def delete_order_item(
    order_item_id: str,
    service: OrderItemService = Depends(get_order_item_service)
):
    """Delete an order item"""
    success = await service.delete_order_item(order_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order item not found")
    return {"message": "Order item deleted successfully"}