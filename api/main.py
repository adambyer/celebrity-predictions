from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.auth import router as auth_router
from .routes.celebrity import router as celebrity_router
from .routes.prediction import router as prediction_router
from .routes.user import router as user_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(celebrity_router)
app.include_router(prediction_router)
app.include_router(user_router)

# TODO: do this when running locally only.
origins = [
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
