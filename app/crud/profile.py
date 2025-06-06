
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from db.mongodb import AsyncIOMotorClient
from core.config import settings
from models.profile import( 
    Country, 
    ProfileInUpdate, 
    ProfileInDB
    )
from datetime import datetime


async def create_profile_for_username(
    conn: AsyncIOMotorClient, 
    username: str, 
    country : Country,
    bio : str,
    image : str
    ) -> ProfileInDB:

    row = await conn[settings.DB_NAME][settings.PROFILES_COLLECTION_NAME].find_one({"username": username})
    if row:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username already has a profile",
        )

    db_profile = ProfileInDB(
        username = username,
        points = 0,
        country = country,
        bio = bio,
        image = image
        )
        

    db_profile.created_at = datetime.now()
    db_profile.updated_at = datetime.now()

    inserted_row = await conn[settings.DB_NAME][settings.PROFILES_COLLECTION_NAME].insert_one(db_profile.dict())
    db_profile.id = str(inserted_row.inserted_id)

    return db_profile


async def get_profile_for_username(conn: AsyncIOMotorClient, username: str) -> ProfileInDB:
    
    row = await conn[settings.DB_NAME][settings.PROFILES_COLLECTION_NAME].find_one({"username": username})
    if not row:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Profile does not exist",
        )
    
    db_profile = ProfileInDB(**row)
    db_profile.id = str(row["_id"])

    return db_profile


async def update_profile_for_username(
        conn: AsyncIOMotorClient, 
        username: str, 
        country : Country,
        bio : str,
        image : str
        ) -> ProfileInDB:

    old_profile = await get_profile_for_username(conn, username)
    new_profile = ProfileInDB(**old_profile.dict())

    new_profile.updated_at = datetime.now()
    new_profile.country = country or old_profile.country
    new_profile.bio = bio or old_profile.bio
    new_profile.image = image or old_profile.image

    await conn[settings.DB_NAME][settings.PROFILES_COLLECTION_NAME].update_one({"username": old_profile.username}, {'$set': new_profile.dict()})
    return ProfileInUpdate(old_profile = old_profile, new_profile = new_profile)

async def delete_profile_for_username(conn: AsyncIOMotorClient, username: str) -> ProfileInDB:
    db_profile = await get_profile_for_username(conn, username)
    try:
        await conn[settings.DB_NAME][settings.PROFILES_COLLECTION_NAME].delete_one({"username": db_profile.username})
    except Exception as e:
        print(e)
    return db_profile


async def add_points_to_profile(conn: AsyncIOMotorClient, current_username: str, points: int):
    try:
        await conn[settings.DB_NAME][settings.PROFILES_COLLECTION_NAME].update_one({"username": current_username}, {'$inc':{"points": points}})
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e
        )