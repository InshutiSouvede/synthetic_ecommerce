from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class CustomerBase(BaseModel):
    name: str
    email: str
    gender: Optional[str]
    signup_date: Optional[date]
    country: Optional[str]

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    customer_id: int
    class Config:
        orm_mode = True



class ProductBase(BaseModel):
    product_name: str
    category: Optional[str]
    price: float
    stock_quantity: Optional[int]
    brand: Optional[str]

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    product_id: int
    class Config:
        orm_mode = True



class OrderBase(BaseModel):
    customer_id: int
    order_date: Optional[date]
    total_amount: float
    payment_method: Optional[str]
    shipping_country: Optional[str]

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    order_id: int
    class Config:
        orm_mode = True



class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    order_item_id: int
    class Config:
        orm_mode = True



class ProductReviewBase(BaseModel):
    product_id: int
    customer_id: int
    rating: int
    review_text: Optional[str]
    review_date: Optional[date]

class ProductReviewCreate(ProductReviewBase):
    pass

class ProductReview(ProductReviewBase):
    review_id: int
    class Config:
        orm_mode = True
