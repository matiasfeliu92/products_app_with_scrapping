import json
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List
from sqlmodel import Session, desc, func, select
from sqlalchemy.orm import joinedload, selectinload

from src.config.db import ManageDB
from src.config.scrapper_settings import ScrapperSettings
from src.core.scrapper import Scrapper
from src.models.brand import Brand
from src.models.category import Category
from src.models.history import History
from src.models.product import Product
from src.models.store import Store
from src.schemas.category_out import CategoryOut
from src.schemas.product_input import ProductInput
from src.schemas.product_scrapped import ProductScraped
from src.schemas.history_out import HistoryOut
from src.schemas.product_with_latest_history import ProductWithLatestHistory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class ProductRoutes:
    def __init__(self):
        self.scrapper_settings = ScrapperSettings()
        self.router = APIRouter(prefix="/products")
        self.router.add_api_route("/", self.get_products, response_model=List[ProductWithLatestHistory], methods=["GET"])
        self.router.add_api_route("/new", self.new_product, response_model=ProductScraped, methods=["POST"])

    def get_products(self, session: Session = Depends(ManageDB().get_session)):
        latest_history_subq = (
            select(
                History.product_id,
                func.max(History.created_at).label("max_created_at")
            )
            .group_by(History.product_id)
            .subquery()
        )

        stmt = (
            select(
                Product.id,
                Product.name,
                Product.sku,
                Brand.name.label("brand"),
                Category.main_category,
                Category.sub_category,
                Store.name.label("store"),
                Product.url,
                History.list_price,
                History.cash_price,
                History.discount_pct,
                History.stock,
                History.installments,
                History.created_at
            )
            .join(Brand, Brand.id == Product.brand_id)
            .join(Category, Category.id == Product.category_id)
            .join(Store, Store.id == Product.store)
            .join(latest_history_subq, latest_history_subq.c.product_id == Product.id)
            .join(
                History,
                (History.product_id == Product.id) &
                (History.created_at == latest_history_subq.c.max_created_at)
            )
        )

        rows = session.exec(stmt).all()
        logging.info("-------------------results-------------------")
        logging.info(rows)
        result = []
        for row in rows:
            data = row._mapping
            logging.info("-------------------data mapped-------------------")
            logging.info(data)
            result.append(
                ProductWithLatestHistory(
                    id=data["id"],
                    name=data["name"],
                    sku=data["sku"],
                    brand=data["brand"],
                    category=CategoryOut(
                        main=data["main_category"],
                        sub=data["sub_category"]
                    ),
                    store=data["store"],
                    url=data["url"],
                    history=HistoryOut(
                        list_price=data["list_price"],
                        cash_price=data["cash_price"],
                        discount_pct=data["discount_pct"],
                        stock=data["stock"],
                        installments=data["installments"],
                        created_at=data["created_at"]
                    )
                )
            )
        return result

    def new_product(self, payload: ProductInput, session: Session = Depends(ManageDB().get_session)):
        logging.info(f"LINK -----> {payload.link}")
        scrapper = Scrapper(str(payload.link))
        product_data = scrapper.extract_data()
        logging.info(f"PRODUCT DATA TYPE -----> {type(product_data)}")
        logging.info(f"PRODUCT DATA -----> {product_data}")

        brand_found = session.scalar(select(Brand).where(Brand.name == product_data["brand"]))
        if brand_found:
            logging.info(f"BRAND FOUND -------> {brand_found}")
            brand_id = brand_found.id
        else:
            brand_to_save = Brand(name=product_data["brand"])
            session.add(brand_to_save)
            session.commit()
            brand_id = brand_to_save.id

        category_found = session.scalar(select(Category).where((Category.main_category == product_data["main_category"]) & (Category.sub_category == product_data["sub_category"])))
        if category_found:
            logging.info(f"BRAND FOUND -------> {category_found}")
            category_id = category_found.id
        else:
            category_to_save = Category(main_category=product_data["main_category"], sub_category=product_data["sub_category"])
            session.add(category_to_save)
            session.commit()
            category_id = category_to_save.id

        store_found = session.scalar(select(Store).where(Store.name == product_data["store"]))
        if store_found:
            logging.info(f"STORE FOUND -------> {store_found}")
            store_id = store_found.id
        else:
            store_to_save = Store(name=product_data["store"])
            session.add(store_to_save)
            session.commit()
            store_id = store_to_save.id

        installments_raw = product_data.get("installments") or {}
        installments_to_save = json.dumps(installments_raw, ensure_ascii=False)

        product_found = session.scalar(select(Product).where(Product.name == product_data["name"]))
        if product_found:
            logging.info(f"PRODUCT FOUND -------> {product_found}")
            product_id = product_found.id
            prod_hist = session.scalar( select(History) .where(History.product_id == product_id) .order_by(desc(History.created_at)) )
            if prod_hist is None or prod_hist.list_price != float(product_data["list_price"]) or prod_hist.cash_price != float(product_data["cash_price"]) or prod_hist.discount_pct != float(product_data["discount_applicated"]):
                logging.info(f"HIST FOUND -------> {prod_hist}")
                logging.info(f'PRECIO ACTUAL --> {type(prod_hist.list_price)}, NUEVO PRECIO --> {type(float(product_data["list_price"]))}')
                logging.info("CAMBIARON LOS PRECIOSS")
                logging.info(prod_hist.list_price != float(product_data["list_price"]))
                logging.info(prod_hist.cash_price != float(product_data["cash_price"]))
                history_to_save = History(list_price=product_data["list_price"], cash_price=product_data["cash_price"], discount_pct=product_data["discount_applicated"], stock=product_data["stock"], installments=installments_to_save, product_id=product_id)
                session.add(history_to_save)
                session.commit()
            else:
                logging.info("PRODUCT HAS NO UPDATES")
        else:
            product_to_save = Product(sku=product_data["sku"], name=product_data["name"], brand_id=brand_id, category_id=category_id, store=store_id, history=[], url=str(payload.link))
            session.add(product_to_save)
            session.commit()
            product_id = product_to_save.id

            history_to_save = History(list_price=product_data["list_price"], cash_price=product_data["cash_price"], discount_pct=product_data["discount_applicated"], stock=product_data["stock"], installments=installments_to_save, product_id=product_id)
            session.add(history_to_save)
            session.commit()
        return JSONResponse(product_data)