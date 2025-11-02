from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers.customers import router as customers_router
from app.routers.products import router as products_router
from app.routers.orders import router as orders_router
from app.routers.order_items import router as order_items_router
from app.routers.reviews import router as reviews_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce API")

app.include_router(customers_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(order_items_router)
app.include_router(reviews_router)
@app.get("/")
def read_root():
    return {"message": "Welcome to the E-Commerce API"}
