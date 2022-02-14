from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engin
from . import models
from .router import post, user, auth, vote
from .config import settings


models.Base.metadata.create_all(bind=engin)


app = FastAPI()
origins = ["https://www.google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
