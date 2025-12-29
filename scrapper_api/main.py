from fastapi import FastAPI

from scrapper_api.src.api.product_routes import ProductRoutes

app = FastAPI()

product_routes = ProductRoutes().router

app.include_router(product_routes)

@app.get("/")
def read_root():
    print("----------------------------")
    return {"Hello": "World"}