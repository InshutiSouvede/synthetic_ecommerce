from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import Product, ProductCreate, ProductUpdate
from .base import convert_objectid_to_string

class ProductService:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.products

    async def create_product(self, product: ProductCreate) -> Product:
        product_dict = product.model_dump()
        result = await self.collection.insert_one(product_dict)
        created_product = await self.collection.find_one({"_id": result.inserted_id})
        created_product = convert_objectid_to_string(created_product)
        return Product(**created_product)

    async def get_product(self, product_id: str) -> Optional[Product]:
        product_data = await self.collection.find_one({"_id": ObjectId(product_id)})
        if product_data:
            product_data = convert_objectid_to_string(product_data)
            return Product(**product_data)
        return None

    async def get_product_by_product_id(self, product_id: int) -> Optional[Product]:
        product_data = await self.collection.find_one({"product_id": product_id})
        if product_data:
            product_data = convert_objectid_to_string(product_data)
            return Product(**product_data)
        return None

    async def get_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        cursor = self.collection.find().skip(skip).limit(limit)
        products = []
        async for product_data in cursor:
            product_data = convert_objectid_to_string(product_data)
            products.append(Product(**product_data))
        return products

    async def get_products_by_category(self, category: str) -> List[Product]:
        cursor = self.collection.find({"category": category})
        products = []
        async for product_data in cursor:
            product_data = convert_objectid_to_string(product_data)
            products.append(Product(**product_data))
        return products

    async def update_product(self, product_id: str, product_update: ProductUpdate) -> Optional[Product]:
        update_data = {k: v for k, v in product_update.model_dump().items() if v is not None}
        if update_data:
            await self.collection.update_one(
                {"_id": ObjectId(product_id)}, 
                {"$set": update_data}
            )
        return await self.get_product(product_id)

    async def delete_product(self, product_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0