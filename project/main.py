from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from project.accounts.admin import UserAdmin
from project.accounts.routers import accounts_router
from project.db_settings import engine
from project.env_config import env

from sqladmin import Admin

app = FastAPI()
app.include_router(accounts_router)


@app.get("/")
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

admin = Admin(app, engine)
admin.add_view(UserAdmin)
