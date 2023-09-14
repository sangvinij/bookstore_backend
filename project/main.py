from fastapi import FastAPI, Depends

from project.accounts.routers import accounts_router

app = FastAPI()
app.include_router(accounts_router)


@app.get('/')
def index():
    return {}
