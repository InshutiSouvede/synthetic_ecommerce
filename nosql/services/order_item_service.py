from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import OrderItem, OrderItemCreate, OrderItemUpdate
from .base import convert_objectid_to_string

class OrderItemService:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.order_items

    async def create_order_item(self, order_item: OrderItemCreate) -> OrderItem:
        order_item_dict = order_item.model_dump()
        result = await self.collection.insert_one(order_item_dict)
        created_order_item = await self.collection.find_one({"_id": result.inserted_id})
        created_order_item = convert_objectid_to_string(created_order_item)
        return OrderItem(**created_order_item)

    async def get_order_item(self, order_item_id: str) -> Optional[OrderItem]:
        order_item_data = await self.collection.find_one({"_id": ObjectId(order_item_id)})
        if order_item_data:
            order_item_data = convert_objectid_to_string(order_item_data)
            return OrderItem(**order_item_data)
        return None

    async def get_order_items(self, skip: int = 0, limit: int = 100) -> List[OrderItem]:
        cursor = self.collection.find().skip(skip).limit(limit)
        order_items = []
        async for order_item_data in cursor:
            order_item_data = convert_objectid_to_string(order_item_data)
            order_items.append(OrderItem(**order_item_data))
        return order_items

    async def get_order_items_by_order(self, order_id: int) -> List[OrderItem]:
        cursor = self.collection.find({"order_id": order_id})
        order_items = []
        async for order_item_data in cursor:
            order_item_data = convert_objectid_to_string(order_item_data)
            order_items.append(OrderItem(**order_item_data))
        return order_items

    async def update_order_item(self, order_item_id: str, order_item_update: OrderItemUpdate) -> Optional[OrderItem]:
        update_data = {k: v for k, v in order_item_update.model_dump().items() if v is not None}
        if update_data:
            await self.collection.update_one(
                {"_id": ObjectId(order_item_id)}, 
                {"$set": update_data}
            )
        return await self.get_order_item(order_item_id)

    async def delete_order_item(self, order_item_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(order_item_id)})
        return result.deleted_count > 0