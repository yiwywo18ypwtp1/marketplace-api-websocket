from fastapi import FastAPI

import app.models

from app.routes.user_router import router as user_router

app = FastAPI()

@app.get("/")
def healthchek():
    return {"message": "API working"}


app.include_router(user_router, prefix="/users", tags=["Auth"])