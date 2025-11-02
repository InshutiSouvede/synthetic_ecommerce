from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import ProductReview, ProductReviewCreate, ProductReviewUpdate
from .base import convert_objectid_to_string

class ProductReviewService:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.product_reviews

    async def create_product_review(self, product_review: ProductReviewCreate) -> ProductReview:
        product_review_dict = product_review.model_dump()
        result = await self.collection.insert_one(product_review_dict)
        created_product_review = await self.collection.find_one({"_id": result.inserted_id})
        created_product_review = convert_objectid_to_string(created_product_review)
        return ProductReview(**created_product_review)

    async def get_product_review(self, review_id: str) -> Optional[ProductReview]:
        review_data = await self.collection.find_one({"_id": ObjectId(review_id)})
        if review_data:
            review_data = convert_objectid_to_string(review_data)
            return ProductReview(**review_data)
        return None

    async def get_product_reviews(self, skip: int = 0, limit: int = 100) -> List[ProductReview]:
        cursor = self.collection.find().skip(skip).limit(limit)
        reviews = []
        async for review_data in cursor:
            review_data = convert_objectid_to_string(review_data)
            reviews.append(ProductReview(**review_data))
        return reviews

    async def get_reviews_by_product(self, product_id: int) -> List[ProductReview]:
        cursor = self.collection.find({"product_id": product_id})
        reviews = []
        async for review_data in cursor:
            review_data = convert_objectid_to_string(review_data)
            reviews.append(ProductReview(**review_data))
        return reviews

    async def get_reviews_by_customer(self, customer_id: int) -> List[ProductReview]:
        cursor = self.collection.find({"customer_id": customer_id})
        reviews = []
        async for review_data in cursor:
            review_data = convert_objectid_to_string(review_data)
            reviews.append(ProductReview(**review_data))
        return reviews

    async def update_product_review(self, review_id: str, review_update: ProductReviewUpdate) -> Optional[ProductReview]:
        update_data = {k: v for k, v in review_update.model_dump().items() if v is not None}
        if update_data:
            await self.collection.update_one(
                {"_id": ObjectId(review_id)}, 
                {"$set": update_data}
            )
        return await self.get_product_review(review_id)

    async def delete_product_review(self, review_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(review_id)})
        return result.deleted_count > 0