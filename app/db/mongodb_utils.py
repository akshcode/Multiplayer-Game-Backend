import logging
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import DB_URL
from db.mongodb import db

async def connect_to_mongo():
    try:
        db.client = AsyncIOMotorClient(str(DB_URL))
        await db.client.server_info()
        logging.info("MongoDB connected.")
    except Exception as e:
        logging.error(f"MongoDB connection failed: {e}")
        raise

async def close_mongo_connection():
    db.client.close()
    logging.info("MongoDB disconnected.")