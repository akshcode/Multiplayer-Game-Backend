from motor.motor_asyncio import AsyncIOMotorClient

class DataBase:
    client: AsyncIOMotorClient = None

db = DataBase()

async def get_database() -> AsyncIOMotorClient:
    if not db.client:
        raise RuntimeError("MongoDB client is not initialized.")
    return db.client