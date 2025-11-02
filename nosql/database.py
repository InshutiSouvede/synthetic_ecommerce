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
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        
        
        connection_options = {
            "serverSelectionTimeoutMS": 10000, 
            "connectTimeoutMS": 10000,
            "socketTimeoutMS": 20000,
            "maxPoolSize": 10,
            "minPoolSize": 1,
        }
        
        if "mongodb+srv://" in mongodb_url:
            connection_options.update({
                "tls": True,
                "tlsAllowInvalidCertificates": True,
                "tlsAllowInvalidHostnames": True,
                "retryWrites": True,
                "w": "majority"
            })
            db.client = AsyncIOMotorClient(mongodb_url, server_api=ServerApi('1'), **connection_options)
        else:
            db.client = AsyncIOMotorClient(mongodb_url, **connection_options)
        
        db.database = db.client[os.getenv("DATABASE_NAME", "ecommerce_db")]

        await db.client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Warning: Failed to connect to MongoDB: {e}")
        print("The API will still start but database operations will fail.")
        if "mongodb+srv://" in os.getenv("MONGODB_URL", ""):
            print("Please check your MongoDB Atlas connection string and network access settings.")
        else:
            print("Please ensure MongoDB is running on mongodb://localhost:27017")

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB!")