from fastapi import FastAPI

import app.models

from app.routes.user_router import router as user_router
from app.routes.product_router import router as product_router

app = FastAPI()

@app.get("/")
def healthchek():
    return {"message": "API working"}


app.include_router(user_router, prefix="/users", tags=["Auth"])
app.include_router(product_router, prefix="/products", tags=["Products"])