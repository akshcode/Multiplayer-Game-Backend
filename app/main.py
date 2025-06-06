import uvicorn
from fastapi import FastAPI
from api.api import router as api_router
from core.config import settings
from db.mongodb_utils import close_mongo_connection, connect_to_mongo
from starlette.middleware.cors import CORSMiddleware
from middlewares.security_headers import SecurityHeadersMiddleware

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)