from fastapi import FastAPI

from .routes.auth import router as auth_router
from .routes.user import router as user_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
