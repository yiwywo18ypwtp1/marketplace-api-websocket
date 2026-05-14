from fastapi import FastAPI

from app.routes.user_router import router as user_router
from app.routes.product_router import router as product_router
from app.routes.order_router import router as order_router

app = FastAPI()

@app.get("/")
def healthchek():
    return {"message": "API working"}


app.include_router(user_router, prefix="/users", tags=["Auth"])
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(order_router, prefix="/orders", tags=["Orders"])