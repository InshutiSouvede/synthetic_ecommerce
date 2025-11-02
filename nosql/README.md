# E-commerce FastAPI Application with MongoDB

This FastAPI application provides CRUD API for e-commerce data management using MongoDB as the database.

## Data Structure

The application manages the following entities based on the CSV data structure:

### Customers
- `customer_id`: Unique customer identifier
- `name`: Customer name
- `email`: Customer email
- `gender`: Customer gender
- `signup_date`: Date when customer signed up
- `country`: Customer's country

### Products
- `product_id`: Unique product identifier
- `product_name`: Product name
- `category`: Product category
- `price`: Product price
- `stock_quantity`: Available stock
- `brand`: Product brand

### Orders
- `order_id`: Unique order identifier
- `customer_id`: Reference to customer
- `order_date`: Date of order
- `total_amount`: Total order amount
- `payment_method`: Payment method used
- `shipping_country`: Shipping destination

### Order Items
- `order_item_id`: Unique order item identifier
- `order_id`: Reference to order
- `product_id`: Reference to product
- `quantity`: Quantity ordered
- `unit_price`: Price per unit

### Product Reviews
- `review_id`: Unique review identifier
- `product_id`: Reference to product
- `customer_id`: Reference to customer
- `rating`: Review rating (1-5)
- `review_text`: Review content
- `review_date`: Date of review

## Requirements

- Python 3.8+
- MongoDB (local or cloud instance)
- FastAPI
- Motor (async MongoDB driver)
- Pydantic

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ecommerce_db
```

3. Make sure MongoDB is running on your system

## Running the Application

1. Start the FastAPI server:
```bash
python main.py
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Customers
- `POST /customers/` - Create a new customer
- `GET /customers/` - Get all customers (with pagination)
- `GET /customers/{customer_id}` - Get customer by MongoDB ObjectId
- `GET /customers/by-customer-id/{customer_id}` - Get customer by customer_id
- `PUT /customers/{customer_id}` - Update customer
- `DELETE /customers/{customer_id}` - Delete customer

### Products
- `POST /products/` - Create a new product
- `GET /products/` - Get all products (with pagination)
- `GET /products/{product_id}` - Get product by MongoDB ObjectId
- `GET /products/by-product-id/{product_id}` - Get product by product_id
- `GET /products/category/{category}` - Get products by category
- `PUT /products/{product_id}` - Update product
- `DELETE /products/{product_id}` - Delete product

### Orders
- `POST /orders/` - Create a new order
- `GET /orders/` - Get all orders (with pagination)
- `GET /orders/{order_id}` - Get order by MongoDB ObjectId
- `GET /orders/by-order-id/{order_id}` - Get order by order_id
- `GET /orders/customer/{customer_id}` - Get orders by customer
- `PUT /orders/{order_id}` - Update order
- `DELETE /orders/{order_id}` - Delete order

### Order Items
- `POST /order-items/` - Create a new order item
- `GET /order-items/` - Get all order items (with pagination)
- `GET /order-items/{order_item_id}` - Get order item by MongoDB ObjectId
- `GET /order-items/order/{order_id}` - Get order items by order
- `PUT /order-items/{order_item_id}` - Update order item
- `DELETE /order-items/{order_item_id}` - Delete order item

### Product Reviews
- `POST /product-reviews/` - Create a new product review
- `GET /product-reviews/` - Get all product reviews (with pagination)
- `GET /product-reviews/{review_id}` - Get review by MongoDB ObjectId
- `GET /product-reviews/product/{product_id}` - Get reviews by product
- `GET /product-reviews/customer/{customer_id}` - Get reviews by customer
- `PUT /product-reviews/{review_id}` - Update product review
- `DELETE /product-reviews/{review_id}` - Delete product review

