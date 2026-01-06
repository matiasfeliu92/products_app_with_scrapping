from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.api.product_routes import ProductRoutes
from src.config.db import ManageDB

class AppCreator:
    def __init__(self):
        self.manage_db = ManageDB()
        self.app = FastAPI(lifespan=self._lifespan)
        self._set_routes()

    @asynccontextmanager
    async def _lifespan(self, app: FastAPI):
        self.manage_db.init_db()
        yield

    def _set_routes(self):
        product_routes = ProductRoutes().router
        self.app.include_router(product_routes)
        
        @self.app.get("/")
        def read_root():
            return {"Hello": "World"}