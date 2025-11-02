from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import Customer, CustomerCreate, CustomerUpdate
from .base import convert_objectid_to_string

class CustomerService:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.customers

    async def create_customer(self, customer: CustomerCreate) -> Customer:
        customer_dict = customer.model_dump()
        result = await self.collection.insert_one(customer_dict)
        created_customer = await self.collection.find_one({"_id": result.inserted_id})
        created_customer = convert_objectid_to_string(created_customer)
        return Customer(**created_customer)

    async def get_customer(self, customer_id: str) -> Optional[Customer]:
        customer_data = await self.collection.find_one({"_id": ObjectId(customer_id)})
        if customer_data:
            customer_data = convert_objectid_to_string(customer_data)
            return Customer(**customer_data)
        return None

    async def get_customer_by_customer_id(self, customer_id: int) -> Optional[Customer]:
        customer_data = await self.collection.find_one({"customer_id": customer_id})
        if customer_data:
            customer_data = convert_objectid_to_string(customer_data)
            return Customer(**customer_data)
        return None

    async def get_customers(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        cursor = self.collection.find().skip(skip).limit(limit)
        customers = []
        async for customer_data in cursor:
            customer_data = convert_objectid_to_string(customer_data)
            customers.append(Customer(**customer_data))
        return customers

    async def update_customer(self, customer_id: str, customer_update: CustomerUpdate) -> Optional[Customer]:
        update_data = {k: v for k, v in customer_update.model_dump().items() if v is not None}
        if update_data:
            await self.collection.update_one(
                {"_id": ObjectId(customer_id)}, 
                {"$set": update_data}
            )
        return await self.get_customer(customer_id)

    async def delete_customer(self, customer_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(customer_id)})
        return result.deleted_count > 0