from fastapi import FastAPI
from app.database import Base, engine
from app.routers import customers, products, orders, order_items, reviews

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce API")

app.include_router(customers.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(order_items.router)
app.include_router(reviews.router)
@app.get("/")
def read_root():
    return {"message": "Welcome to the E-Commerce API"}