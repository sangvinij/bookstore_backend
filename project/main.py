from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from project.accounts.routers import accounts_router
from project.env_config import env

app = FastAPI()
app.include_router(accounts_router)


@app.get('/')
def index():
    return {}


origins = env.ALLOWED_HOSTS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
