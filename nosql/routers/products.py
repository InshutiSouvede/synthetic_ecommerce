from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import get_database
from models import Product, ProductCreate, ProductUpdate
from services import ProductService

router = APIRouter(prefix="/products", tags=["products"])

def get_product_service(database: AsyncIOMotorDatabase = Depends(get_database)) -> ProductService:
    return ProductService(database)

@router.post("/", response_model=Product)
async def create_product(
    product: ProductCreate,
    service: ProductService = Depends(get_product_service)
):
    """Create a new product"""
    return await service.create_product(product)

@router.get("/", response_model=List[Product])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: ProductService = Depends(get_product_service)
):
    """Get all products with pagination"""
    return await service.get_products(skip=skip, limit=limit)

@router.get("/category/{category}", response_model=List[Product])
async def get_products_by_category(
    category: str,
    service: ProductService = Depends(get_product_service)
):
    """Get products by category"""
    return await service.get_products_by_category(category)

@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: str,
    service: ProductService = Depends(get_product_service)
):
    """Get a product by MongoDB ObjectId"""
    product = await service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/by-product-id/{product_id}", response_model=Product)
async def get_product_by_product_id(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    """Get a product by their product_id"""
    product = await service.get_product_by_product_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: str,
    product_update: ProductUpdate,
    service: ProductService = Depends(get_product_service)
):
    """Update a product"""
    product = await service.update_product(product_id, product_update)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    service: ProductService = Depends(get_product_service)
):
    """Delete a product"""
    success = await service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}