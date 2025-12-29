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
            product_title = self.extract_elements.safe_find_elements(By.TAG_NAME, self.settings.MEXX_SELECTORS["PRODUCT_TITLE"])
            sku = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.MEXX_SELECTORS["SKU"])
            brand = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.MEXX_SELECTORS["BRAND"])
            category_path = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.MEXX_SELECTORS["CATEGORY_PATH"])
            category_path_elements = [li.text for li in category_path.find_elements(By.TAG_NAME, "li")]
            list_price = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.MEXX_SELECTORS["LIST_PRICE"])
            cash_price = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.MEXX_SELECTORS["CASH_PRICE"])
            discount_applicated = 100 - ((float(cash_price.text.replace("$", "").replace(".", ""))/float(list_price.text.replace("$", "").replace(".", ""))) * 100)
            installments = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.MEXX_SELECTORS["INSTALLMENTS"])
            stock = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.MEXX_SELECTORS["STOCK"])
            warranty = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.MEXX_SELECTORS["WARRANTY"])

            self.product_data["name"] = product_title.text if product_title else ""
            self.product_data["sku"] = sku.text.replace("CÓDIGO:", "") if sku else ""
            self.product_data["brand"] = brand.text.replace("Marca : ", "") if brand else ""
            self.product_data["main_category"] = category_path_elements[1] if len(category_path_elements)>1 else ""
            self.product_data["sub_category"] = category_path_elements[2] if len(category_path_elements)>2 else ""
            self.product_data["list_price"] = list_price.text if list_price else ""
            self.product_data["cash_price"] = cash_price.text if cash_price else ""
            self.product_data["discount_applicated"] = round(discount_applicated, 2)
            self.product_data["installments"] = installments.text if installments and type(installments) != list else ""
            self.product_data["stock"] = "Available" if "EN STOCK" in stock.text else "Not Available"
            self.product_data["warranty"] = warranty.text if warranty else ""
            self.product_data["store"] = "Mexx"
            logging.info(f"------------PRODUCT DATA------------>{self.product_data}")
            logging.info(
                "---------------------------------------------------------------------------------------------------"
            )
            logging.info("")
            logging.info("")
            return self.product_data

        elif "fullh4rd.com.ar" in self.link:
            logging.info(
                    "---------------------------------------------------------------------------------------------------"
                )
            logging.info(f"ACCEDIENDO A {self.link}")
            logging.info(self.driver)
            self.driver.get(self.link)
            time.sleep(random.uniform(2, 5))
            product_title = self.extract_elements.safe_find_elements(By.TAG_NAME, self.settings.FULLH4RD_SELECTORS["PRODUCT_TITLE"])
            sku = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.FULLH4RD_SELECTORS["SKU"])
            category_path = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.FULLH4RD_SELECTORS["CATEGORY_PATH"], multiple=True)
            installments = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.FULLH4RD_SELECTORS["INSTALLMENTS"], multiple=True)
            installments_text = [p.text.strip() for p in installments]
            logging.info(f"PRODUCTS INSTALMENTS ----> {installments_text}")
            installments_options = {}
            calculate_list_price = 0
            for i, elem in enumerate(installments_text):
                split_elem = elem.split(": ")
                installments_options_text = [instalment[0:8] for instalment in split_elem if "cuotas" in instalment]
                installments_options[f"option {i+1}"] = installments_options_text[0]
                logging.info(f"SPLITED INSTALMENTS ----> {split_elem}")
                logging.info(f"INSTALLMENTS OPTIONS TEXT ----> {installments_options_text}")
                if any("6 cuotas" in part for part in split_elem):
                    n_instalments = int(split_elem[0][0])
                    instalment_price = float(split_elem[1].replace("$", "").replace(".", "").replace(",", "."))
                    calculate_list_price = n_instalments * instalment_price
            cash_price = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.FULLH4RD_SELECTORS["CASH_PRICE"])
            discount_applicated = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.FULLH4RD_SELECTORS["DISCOUNT_APPLICATED"])
            web_stock = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.FULLH4RD_SELECTORS["WEB_STOCK"])
            local_stock = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.FULLH4RD_SELECTORS["LOCAL_STOCK"])
            logging.info(f"WEB STOCK ----> {web_stock.text}, LOCAL STOCK ----> {local_stock.text}")
            warranty = self.extract_elements.safe_find_elements(By.XPATH, self.settings.FULLH4RD_SELECTORS["WARRANTY"])

            self.product_data["name"] = product_title.text if product_title else ""
            self.product_data["sku"] = sku.text if sku else ""
            self.product_data["brand"] = category_path[2].text if len(category_path)>1 else ""
            self.product_data["main_category"] = category_path[1].text if len(category_path)>1 else ""
            self.product_data["sub_category"] = category_path[2].text if len(category_path)>2 else ""
            self.product_data["list_price"] = calculate_list_price
            self.product_data["cash_price"] = cash_price.text if cash_price else ""
            self.product_data["discount_applicated"] = discount_applicated.text if discount_applicated else ""
            self.product_data["installments"] = installments_options
            self.product_data["stock"] = "Available" if "SIN STOCK" not in web_stock.text or "SIN STOCK" not in local_stock.text else "Not Available"
            self.product_data["warranty"] = warranty.text if warranty else ""
            self.product_data["store"] = "Fullh4rd"
            logging.info(f"------------PRODUCT DATA------------>{self.product_data}")
            logging.info(
                "---------------------------------------------------------------------------------------------------"
            )
            logging.info("")
            logging.info("")
            return self.product_data

        elif "datasoft.com.ar" in self.link:
            logging.info(
                    "---------------------------------------------------------------------------------------------------"
                )
            logging.info(f"ACCEDIENDO A {self.link}")
            logging.info(self.driver)
            self.driver.get(self.link)
            time.sleep(random.uniform(2, 5))
            product_title = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.DATASOFT_SELECTORS["PRODUCT_TITLE"])
            sku = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.DATASOFT_SELECTORS["SKU"])
            brand = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.DATASOFT_SELECTORS["BRAND"])
            category_path = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.DATASOFT_SELECTORS["CATEGORY_PATH"], multiple=True)
            list_price = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.DATASOFT_SELECTORS["LIST_PRICE"])
            cash_price = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.DATASOFT_SELECTORS["CASH_PRICE"])
            discount_applicated = 100 - ((float(cash_price.text.replace("$", "").replace(".", ""))/float(list_price.text.replace(".", ""))) * 100)
            installments = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.settings.DATASOFT_SELECTORS["INSTALLMENTS"])
            n_instalments = [int(n) for n in re.findall(r"\d+", installments.text)]
            installments_options = {}
            for i, inst in enumerate(n_instalments):
                installments_options[f"option {i+1}"] = f"{inst} cuotas"
            warranty = self.extract_elements.safe_find_elements(By.XPATH, self.settings.DATASOFT_SELECTORS["WARRANTY"])

            self.product_data["name"] = product_title.text if product_title else ""
            self.product_data["sku"] = sku.text if brand else ""
            self.product_data["brand"] = brand.text if brand else ""
            self.product_data["main_category"] = category_path[1].text if len(category_path)>1 else ""
            self.product_data["sub_category"] = category_path[2].text if len(category_path)>2 else ""
            self.product_data["list_price"] = list_price.text if list_price else ""
            self.product_data["cash_price"] = cash_price.text if cash_price else ""
            self.product_data["discount_applicated"] = round(discount_applicated, 2)
            self.product_data["installments"] = installments_options
            self.product_data["stock"] = "Available"
            self.product_data["warranty"] = warranty.text if warranty else ""
            self.product_data["store"] = "Datasoft"
            logging.info(f"------------PRODUCT DATA------------>{self.product_data}")
            logging.info(
                "---------------------------------------------------------------------------------------------------"
            )
            logging.info("")
            logging.info("")
            return self.product_data