from typing import Optional, List
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
)
from db.mongodb import AsyncIOMotorClient
from core.config import settings
from models.profile import ProfileInFollow
from crud.profile import get_profile_for_username



async def follow_profile(
    conn: AsyncIOMotorClient, 
    current_username: str, 
    target_username: str
) -> ProfileInFollow:
    target_profile = await get_profile_for_username(conn, target_username)

    if target_profile:
        await conn[settings.DB_NAME][settings.FOLLOWERS_COLLECTION_NAME].insert_one({"follower": current_username,
                                                                          "following": target_profile.username})
    else:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"User {target_username} not found"
        )

    return ProfileInFollow(username= target_profile.username, points = target_profile.points)
    


async def get_follower_list(conn: AsyncIOMotorClient, current_username: str) -> List[str]:
    cursor = conn[settings.DB_NAME][settings.FOLLOWERS_COLLECTION_NAME].find({"following": current_username})

    if not cursor:
        followers = []
    else:
        followers = await cursor.distinct(key = "follower")

    return followers


async def get_following_list(conn: AsyncIOMotorClient, current_username: str) -> List[str]:
    cursor = conn[settings.DB_NAME][settings.FOLLOWERS_COLLECTION_NAME].find({"follower": current_username})

    if not cursor:
        following = []
    else:
        following = await cursor.distinct(key = "following")

    return following


async def get_followers_count(conn: AsyncIOMotorClient, current_username: str) -> int:
    follower_count = await conn[settings.DB_NAME][settings.FOLLOWERS_COLLECTION_NAME].count_documents({"following": current_username})
    return follower_count


async def get_following_count(conn: AsyncIOMotorClient, current_username: str) -> int:
    following_count = await conn[settings.DB_NAME][settings.FOLLOWERS_COLLECTION_NAME].count_documents({"follower": current_username})
    return following_count


async def unfollow_profile(conn: AsyncIOMotorClient, current_username: str, target_username: str) -> ProfileInFollow:
    await conn[settings.DB_NAME][settings.FOLLOWERS_COLLECTION_NAME].delete_many({"follower": current_username,
                                                                     "following": target_username})


async def is_following_profile(conn: AsyncIOMotorClient, current_username: str, target_username: str) -> bool:
    row = await conn[settings.DB_NAME][settings.FOLLOWERS_COLLECTION_NAME].find_one({
                                                                        "follower": current_username,
                                                                        "following": target_username
                                                                        })
    if row:
        return True
    else:
        return False
