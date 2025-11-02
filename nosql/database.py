from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
import ssl
import certifi
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
        
        if "mongodb+srv://" in mongodb_url or "ssl=true" in mongodb_url:
            connection_strategies = [
                {
                    "serverSelectionTimeoutMS": 30000,
                    "connectTimeoutMS": 30000,
                    "socketTimeoutMS": 30000,
                    "maxPoolSize": 10,
                    "minPoolSize": 1,
                    "retryWrites": True,
                    "tls": True,
                    "tlsAllowInvalidCertificates": True,
                    "tlsAllowInvalidHostnames": True,
                    "authSource": "admin",
                },
                {
                    "serverSelectionTimeoutMS": 20000,
                    "connectTimeoutMS": 20000,
                    "socketTimeoutMS": 20000,
                    "maxPoolSize": 5,
                    "retryWrites": True,
                    "ssl": True,
                    "tlsInsecure": True,
                    "authSource": "admin",
                },
                {
                    "serverSelectionTimeoutMS": 15000,
                    "connectTimeoutMS": 15000,
                    "socketTimeoutMS": 15000,
                    "maxPoolSize": 5,
                    "retryWrites": True,
                    "tls": True,
                    "tlsCAFile": certifi.where(),
                    "authSource": "admin",
                },
                {
                    "serverSelectionTimeoutMS": 15000,
                    "connectTimeoutMS": 15000,
                    "socketTimeoutMS": 15000,
                    "maxPoolSize": 5,
                    "retryWrites": True,
                    "authSource": "admin",
                }
            ]
            
            for i, options in enumerate(connection_strategies, 1):
                try:
                    print(f"Attempting connection strategy {i}...")
                    db.client = AsyncIOMotorClient(mongodb_url, **options)
                    await db.client.admin.command('ping')
                    print(f"Successfully connected using strategy {i}!")
                    break
                except Exception as e:
                    print(f"Strategy {i} failed: {str(e)[:100]}...")
                    if i == len(connection_strategies):
                        # Last strategy failed, try with ServerApi as final attempt
                        try:
                            print("Trying final attempt with ServerApi...")
                            final_options = {
                                "serverSelectionTimeoutMS": 10000,
                                "connectTimeoutMS": 10000,
                                "socketTimeoutMS": 10000,
                                "retryWrites": True,
                            }
                            db.client = AsyncIOMotorClient(mongodb_url, server_api=ServerApi('1'), **final_options)
                            await db.client.admin.command('ping')
                            print("Connected with ServerApi!")
                            break
                        except Exception as final_e:
                            raise Exception(f"All connection strategies failed. Last error: {final_e}")
        else:
            connection_options = {
                "serverSelectionTimeoutMS": 30000,
                "connectTimeoutMS": 30000,
                "socketTimeoutMS": 30000,
                "maxPoolSize": 10,
                "minPoolSize": 1,
                "retryWrites": True,
            }
            db.client = AsyncIOMotorClient(mongodb_url, **connection_options)
            await db.client.admin.command('ping')
        
        db.database = db.client[os.getenv("DATABASE_NAME", "ecommerce_db")]
        print("Successfully connected to MongoDB!")
        
    except Exception as e:
        print(f"Warning: Failed to connect to MongoDB: {e}")
        if "mongodb+srv://" in os.getenv("MONGODB_URL", ""):
            print("6. Try adding '?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true' to your connection string")

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB!")