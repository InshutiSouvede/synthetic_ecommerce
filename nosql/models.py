from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CustomerBase(BaseModel):
    customer_id: int
    name: str
    email: str
    gender: str
    signup_date: datetime
    country: str

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    signup_date: Optional[datetime] = None
    country: Optional[str] = None

class Customer(CustomerBase):
    id: Optional[str] = Field(default=None, alias="_id")

class ProductBase(BaseModel):
    product_id: int
    product_name: str
    category: str
    price: float
    stock_quantity: int
    brand: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    brand: Optional[str] = None

class Product(ProductBase):
    id: Optional[str] = Field(default=None, alias="_id")

class OrderBase(BaseModel):
    order_id: int
    customer_id: int
    order_date: datetime
    total_amount: float
    payment_method: str
    shipping_country: str

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    order_date: Optional[datetime] = None
    total_amount: Optional[float] = None
    payment_method: Optional[str] = None
    shipping_country: Optional[str] = None

class Order(OrderBase):
    id: Optional[str] = Field(default=None, alias="_id")

class OrderItemBase(BaseModel):
    order_item_id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    order_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None

class OrderItem(OrderItemBase):
    id: Optional[str] = Field(default=None, alias="_id")

class ProductReviewBase(BaseModel):
    review_id: int
    product_id: int
    customer_id: int
    rating: int
    review_text: str
    review_date: datetime

class ProductReviewCreate(ProductReviewBase):
    pass

class ProductReviewUpdate(BaseModel):
    product_id: Optional[int] = None
    customer_id: Optional[int] = None
    rating: Optional[int] = None
    review_text: Optional[str] = None
    review_date: Optional[datetime] = None

class ProductReview(ProductReviewBase):
    id: Optional[str] = Field(default=None, alias="_id")