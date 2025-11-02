from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import Order, OrderCreate, OrderUpdate
from .base import convert_objectid_to_string

class OrderService:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.orders

    async def create_order(self, order: OrderCreate) -> Order:
        order_dict = order.model_dump()
        result = await self.collection.insert_one(order_dict)
        created_order = await self.collection.find_one({"_id": result.inserted_id})
        created_order = convert_objectid_to_string(created_order)
        return Order(**created_order)

    async def get_order(self, order_id: str) -> Optional[Order]:
        order_data = await self.collection.find_one({"_id": ObjectId(order_id)})
        if order_data:
            order_data = convert_objectid_to_string(order_data)
            return Order(**order_data)
        return None

    async def get_order_by_order_id(self, order_id: int) -> Optional[Order]:
        order_data = await self.collection.find_one({"order_id": order_id})
        if order_data:
            order_data = convert_objectid_to_string(order_data)
            return Order(**order_data)
        return None

    async def get_orders(self, skip: int = 0, limit: int = 100) -> List[Order]:
        cursor = self.collection.find().skip(skip).limit(limit)
        orders = []
        async for order_data in cursor:
            order_data = convert_objectid_to_string(order_data)
            orders.append(Order(**order_data))
        return orders

    async def get_orders_by_customer(self, customer_id: int) -> List[Order]:
        cursor = self.collection.find({"customer_id": customer_id})
        orders = []
        async for order_data in cursor:
            order_data = convert_objectid_to_string(order_data)
            orders.append(Order(**order_data))
        return orders

    async def update_order(self, order_id: str, order_update: OrderUpdate) -> Optional[Order]:
        update_data = {k: v for k, v in order_update.model_dump().items() if v is not None}
        if update_data:
            await self.collection.update_one(
                {"_id": ObjectId(order_id)}, 
                {"$set": update_data}
            )
        return await self.get_order(order_id)

    async def delete_order(self, order_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(order_id)})
        return result.deleted_count > 0