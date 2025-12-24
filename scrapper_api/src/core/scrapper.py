import logging
import random
import re
import time
from selenium.webdriver.common.by import By

from src.config.settings import Settings
from src.utils.extract_elements import ExtractElements

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class Scrapper:
    def __init__(self, __link__):
        self.link = __link__
        self.product_data = {}
        self.settings = Settings()
        self.driver = self.settings.get_chrome_driver()
        self.extract_elements = ExtractElements(self.driver)

    def extract_data(self):
        if "mexx.com.ar" in self.link:
            logging.info(
                    "---------------------------------------------------------------------------------------------------"
                )
            logging.info(f"ACCEDIENDO A {self.link}")
            logging.info(self.driver)
            self.driver.get(self.link)
            time.sleep(random.uniform(2, 5))
            product_title = self.extract_elements.safe_find_elements(By.TAG_NAME, "h1")
            sku = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, "#prod_desc_edit > div.row.pr-0.pl-0.filaMarcas > div > h6:nth-child(2)")
            brand = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, "body > div.section.single.ecommerce-page.mt-0.pt-0 > div > div > div:nth-child(9) > div:nth-child(3) > span:nth-child(1) > p")
            category_path = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, "div.col-md-12.pt-2.pb-2 > ul.breadcrum.nav.navbar-nav.navbar-left")
            category_path_elements = [li.text for li in category_path.find_elements(By.TAG_NAME, "li")]

            self.product_data["name"] = product_title.text if product_title else ""
            self.product_data["sku"] = sku.text.replace("CÓDIGO:", "") if sku else ""
            self.product_data["brand"] = brand.text.replace("Marca : ", "") if brand else ""
            self.product_data["main_category"] = category_path_elements[1] if len(category_path_elements)>1 else ""
            self.product_data["sub_category"] = category_path_elements[2] if len(category_path_elements)>2 else ""
            logging.info(f"------------PRODUCT DATA------------>{self.product_data}")
            logging.info(
                "---------------------------------------------------------------------------------------------------"
            )
            logging.info("")
            logging.info("")

        elif "fullh4rd.com.ar" in self.link:
            logging.info(
                    "---------------------------------------------------------------------------------------------------"
                )
            logging.info(f"ACCEDIENDO A {self.link}")
            logging.info(self.driver)
            self.driver.get(self.link)
            time.sleep(random.uniform(2, 5))
            product_title = self.extract_elements.safe_find_elements(By.TAG_NAME, "h1")
            sku = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, "p.codebar")
            category_path = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, 'a > span[itemprop="item"] > span[itemprop="name"]', multiple=True)

            self.product_data["name"] = product_title.text if product_title else ""
            self.product_data["sku"] = sku.text if sku else ""
            self.product_data["brand"] = category_path[2].text if len(category_path)>1 else ""
            self.product_data["main_category"] = category_path[1].text if len(category_path)>1 else ""
            self.product_data["sub_category"] = category_path[2].text if len(category_path)>2 else ""
            logging.info(f"------------PRODUCT DATA------------>{self.product_data}")
            logging.info(
                "---------------------------------------------------------------------------------------------------"
            )
            logging.info("")
            logging.info("")

        elif "datasoft.com.ar" in self.link:
            logging.info(
                    "---------------------------------------------------------------------------------------------------"
                )
            logging.info(f"ACCEDIENDO A {self.link}")
            logging.info(self.driver)
            self.driver.get(self.link)
            time.sleep(random.uniform(2, 5))
            product_title = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, "h1 > span")
            sku = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, 'span[itemprop="sku"]')
            brand = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, 'div.short_desc > ul > li:nth-child(1)')
            category_path = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, 'div.col-xs-12 > ul.breadcrumb > li > span > a[itemprop="url"] > span[itemprop="title"]', multiple=True)

            self.product_data["name"] = product_title.text if product_title else ""
            self.product_data["sku"] = sku.text if brand else ""
            self.product_data["brand"] = brand.text if brand else ""
            self.product_data["main_category"] = category_path[1].text if len(category_path)>1 else ""
            self.product_data["sub_category"] = category_path[2].text if len(category_path)>2 else ""
            logging.info(f"------------PRODUCT DATA------------>{self.product_data}")
            logging.info(
                "---------------------------------------------------------------------------------------------------"
            )
            logging.info("")
            logging.info("")