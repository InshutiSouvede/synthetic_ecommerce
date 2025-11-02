from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import get_database
from models import ProductReview, ProductReviewCreate, ProductReviewUpdate
from services import ProductReviewService

router = APIRouter(prefix="/product-reviews", tags=["product-reviews"])

def get_product_review_service(database: AsyncIOMotorDatabase = Depends(get_database)) -> ProductReviewService:
    return ProductReviewService(database)

@router.post("/", response_model=ProductReview)
async def create_product_review(
    product_review: ProductReviewCreate,
    service: ProductReviewService = Depends(get_product_review_service)
):
    """Create a new product review"""
    return await service.create_product_review(product_review)

@router.get("/", response_model=List[ProductReview])
async def get_product_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: ProductReviewService = Depends(get_product_review_service)
):
    """Get all product reviews with pagination"""
    return await service.get_product_reviews(skip=skip, limit=limit)

@router.get("/product/{product_id}", response_model=List[ProductReview])
async def get_reviews_by_product(
    product_id: int,
    service: ProductReviewService = Depends(get_product_review_service)
):
    """Get reviews by product ID"""
    return await service.get_reviews_by_product(product_id)

@router.get("/customer/{customer_id}", response_model=List[ProductReview])
async def get_reviews_by_customer(
    customer_id: int,
    service: ProductReviewService = Depends(get_product_review_service)
):
    """Get reviews by customer ID"""
    return await service.get_reviews_by_customer(customer_id)

@router.get("/{review_id}", response_model=ProductReview)
async def get_product_review(
    review_id: str,
    service: ProductReviewService = Depends(get_product_review_service)
):
    """Get a product review by MongoDB ObjectId"""
    review = await service.get_product_review(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Product review not found")
    return review

@router.put("/{review_id}", response_model=ProductReview)
async def update_product_review(
    review_id: str,
    review_update: ProductReviewUpdate,
    service: ProductReviewService = Depends(get_product_review_service)
):
    """Update a product review"""
    review = await service.update_product_review(review_id, review_update)
    if not review:
        raise HTTPException(status_code=404, detail="Product review not found")
    return review

@router.delete("/{review_id}")
async def delete_product_review(
    review_id: str,
    service: ProductReviewService = Depends(get_product_review_service)
):
    """Delete a product review"""
    success = await service.delete_product_review(review_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product review not found")
    return {"message": "Product review deleted successfully"}