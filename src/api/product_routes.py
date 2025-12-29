import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List

from src.config.settings import Settings
from src.core.scrapper import Scrapper
from src.schemas.product_input import ProductInput
from src.schemas.product_scrapped import ProductScraped

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class ProductRoutes:
    def __init__(self):
        self.settings = Settings()
        self.router = APIRouter(prefix="/products")
        self.router.add_api_route("/new", self.new_product, response_model=ProductScraped, methods=["POST"])

    def new_product(self, payload: ProductInput):
        logging.info(f"LINK -----> {payload.link}")
        scrapper = Scrapper(str(payload.link))
        product_data = scrapper.extract_data()
        logging.info(f"PRODUCT DATA -----> {product_data}")
        return JSONResponse(product_data)