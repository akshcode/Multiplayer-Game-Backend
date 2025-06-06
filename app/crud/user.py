from db.mongodb import AsyncIOMotorClient
from pydantic import EmailStr
from core.config import settings
from models.user import UserInRegister, UserInDB, UserInUpdate, UserInLogin, UserInDB, User
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.exceptions import HTTPException
from datetime import datetime


async def get_user(conn: AsyncIOMotorClient, username: str) -> UserInDB:
    row = await conn[settings.DB_NAME][settings.USERS_COLLECTION_NAME].find_one({"username": username})
    if row:
        dbuser = UserInDB(**row)
        dbuser.id = str(row["_id"])
        return dbuser

async def get_user_by_email(conn: AsyncIOMotorClient, email: EmailStr) -> UserInDB:
    row = await conn[settings.DB_NAME][settings.USERS_COLLECTION_NAME].find_one({"email": email})
    if row:
        dbuser = UserInDB(**row)
        dbuser.id = str(row["_id"])
        return dbuser

async def create_user(conn: AsyncIOMotorClient, user: UserInRegister) -> UserInDB:
    dbuser = UserInDB(**user.dict())
    dbuser.change_password(user.password)
    dbuser.created_at = datetime.now()
    dbuser.updated_at = datetime.now()

    inserted_row = await conn[settings.DB_NAME][settings.USERS_COLLECTION_NAME].insert_one(dbuser.dict())
    dbuser.id = str(inserted_row.inserted_id)

    return dbuser

async def update_user(conn: AsyncIOMotorClient, username: str, user: UserInUpdate) -> UserInDB:
    dbuser = await get_user(conn, username)

    dbuser.username = user.username or dbuser.username
    dbuser.email = user.email or dbuser.email

    if user.password:
        dbuser.change_password(user.password)

    dbuser.updated_at = datetime.now()
    await conn[settings.DB_NAME][settings.USERS_COLLECTION_NAME].update_one({"username": dbuser.username}, {'$set': dbuser.dict()})
    return dbuser


async def delete_user(conn: AsyncIOMotorClient, user : UserInLogin) -> UserInDB:
    dbuser = await get_user(conn, user.username)
    try:
        await conn[settings.DB_NAME][settings.USERS_COLLECTION_NAME].delete_one({"email": user.email})
    except Exception as e:
        print(e)

    return dbuser


async def verify_user(conn: AsyncIOMotorClient, user : UserInLogin, current_user: User) -> UserInDB:
    dbuser = await get_user(conn, current_user.username)

    if not dbuser or not dbuser.check_password(user.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
        )
        
    if current_user.username != dbuser.username:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid username"
        )

    return dbuser