from typing import Optional, List
from fastapi.param_functions import Query
from starlette.exceptions import HTTPException
from db.mongodb import AsyncIOMotorClient
from core.config import settings
from models.profile import Country, ProfileInLeaderboard


async def get_leaderboard(
    conn: AsyncIOMotorClient, 
    by_country : Country,
    length:int
    ) -> List[ProfileInLeaderboard]:

    cursor_list = []
    if by_country:
        leaderboard_cursor = conn[settings.DB_NAME][settings.PROFILES_COLLECTION_NAME].find({"country": by_country}, { "username": 1, "country": 1, "points": 1}).sort([("points", -1)])
        cursor_list = await leaderboard_cursor.to_list(length = length)
    else:
        leaderboard_cursor = conn[settings.DB_NAME][settings.PROFILES_COLLECTION_NAME].find({},{ "username": 1, "country": 1, "points": 1}).sort([("points", -1)])
        cursor_list = await leaderboard_cursor.to_list(length = length)
    
    leaderboard = []

    for profile in cursor_list:
        print(profile)
        profile_in_leaderboard = ProfileInLeaderboard(**profile)
        leaderboard.append(profile_in_leaderboard)
    return leaderboard