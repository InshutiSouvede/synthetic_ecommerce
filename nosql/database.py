from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def get_database() -> AsyncIOMotorClient:
    return db.database

async def connect_to_mongo():
    """Create database connection"""
    try:
        db.client = AsyncIOMotorClient(
            os.getenv("MONGODB_URL", "mongodb://localhost:27017"),
            server_api=ServerApi('1'),
            serverSelectionTimeoutMS=5000 
        )
        db.database = db.client[os.getenv("DATABASE_NAME", "ecommerce_db")]

        await db.client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Warning: Failed to connect to MongoDB: {e}")
        print("The API will still start but database operations will fail.")
        print("Please ensure MongoDB is running on mongodb://localhost:27017")

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB!")