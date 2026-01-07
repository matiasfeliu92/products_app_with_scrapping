import logging
import random
import re
import time
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs

from src.config.scrapper_settings import ScrapperSettings
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
        self.scrapper_settings = ScrapperSettings()
        self.driver = self.scrapper_settings.get_chrome_driver()
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
            product_title = self.extract_elements.safe_find_elements(By.TAG_NAME, self.scrapper_settings.MEXX_SELECTORS["PRODUCT_TITLE"])
            sku = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.MEXX_SELECTORS["SKU"])
            brand = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.MEXX_SELECTORS["BRAND"])
            category_path = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.MEXX_SELECTORS["CATEGORY_PATH"])
            category_path_elements = [li.text for li in category_path.find_elements(By.TAG_NAME, "li")]
            list_price = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.MEXX_SELECTORS["LIST_PRICE"])
            cash_price = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.MEXX_SELECTORS["CASH_PRICE"])
            discount_applicated = 100 - ((float(cash_price.text.replace("$", "").replace(".", ""))/float(list_price.text.replace("$", "").replace(".", ""))) * 100)
            installments = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.MEXX_SELECTORS["INSTALLMENTS"])
            stock = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.MEXX_SELECTORS["STOCK"])

            self.product_data["name"] = product_title.text if product_title else ""
            self.product_data["sku"] = sku.text.replace("CÓDIGO:", "") if sku else ""
            self.product_data["brand"] = brand.text.replace("Marca : ", "") if brand else ""
            self.product_data["main_category"] = category_path_elements[1] if len(category_path_elements)>1 else ""
            self.product_data["sub_category"] = category_path_elements[2] if len(category_path_elements)>2 else ""
            self.product_data["list_price"] = list_price.text.replace("$", "").replace(".", "") if list_price else ""
            self.product_data["cash_price"] = cash_price.text.replace("$", "").replace(".", "") if cash_price else ""
            self.product_data["discount_applicated"] = round(discount_applicated, 2)
            self.product_data["installments"] = installments.text if installments and type(installments) != list else ""
            self.product_data["stock"] = "Available" if "EN STOCK" in stock.text else "Not Available"
            self.product_data["warranty"] = ""
            self.product_data["store"] = "Mexx"
            self.product_data["link"] = self.link
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
            product_title = self.extract_elements.safe_find_elements(By.TAG_NAME, self.scrapper_settings.FULLH4RD_SELECTORS["PRODUCT_TITLE"])
            sku = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.FULLH4RD_SELECTORS["SKU"])
            category_path = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.FULLH4RD_SELECTORS["CATEGORY_PATH"], multiple=True)
            installments = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.FULLH4RD_SELECTORS["INSTALLMENTS"], multiple=True)
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
            cash_price = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.FULLH4RD_SELECTORS["CASH_PRICE"])
            discount_applicated = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.FULLH4RD_SELECTORS["DISCOUNT_APPLICATED"])
            web_stock = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.FULLH4RD_SELECTORS["WEB_STOCK"])
            local_stock = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.FULLH4RD_SELECTORS["LOCAL_STOCK"])
            if web_stock is not None:
                logging.info(f"WEB STOCK ----> {web_stock.text}")
            elif local_stock is not None:
                logging.info(f"LOCAL STOCK ----> {local_stock.text}")

            self.product_data["name"] = product_title.text if product_title else ""
            self.product_data["sku"] = sku.text if sku else ""
            self.product_data["brand"] = category_path[2].text if len(category_path)>1 else ""
            self.product_data["main_category"] = category_path[1].text if len(category_path)>1 else ""
            self.product_data["sub_category"] = category_path[2].text if len(category_path)>2 else ""
            self.product_data["list_price"] = calculate_list_price
            self.product_data["cash_price"] = cash_price.text.replace("$", "").replace(".", "").replace(",", ".") if cash_price else ""
            self.product_data["discount_applicated"] = discount_applicated.text.replace("% OFF", "") if discount_applicated else ""
            self.product_data["installments"] = installments_options
            self.product_data["stock"] = "Available" if "SIN STOCK" not in web_stock.text or "SIN STOCK" not in local_stock.text else "Not Available"
            self.product_data["warranty"] = ""
            self.product_data["store"] = "Fullh4rd"
            self.product_data["link"] = self.link
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
            product_title = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.DATASOFT_SELECTORS["PRODUCT_TITLE"])
            sku = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.DATASOFT_SELECTORS["SKU"])
            brand = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.DATASOFT_SELECTORS["BRAND"])
            category_path = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.DATASOFT_SELECTORS["CATEGORY_PATH"], multiple=True)
            list_price = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.DATASOFT_SELECTORS["LIST_PRICE"])
            cash_price = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.DATASOFT_SELECTORS["CASH_PRICE"])
            discount_applicated = 100 - ((float(cash_price.text.replace("$", "").replace(".", ""))/float(list_price.text.replace(".", ""))) * 100)
            installments = self.extract_elements.safe_find_elements(By.CSS_SELECTOR, self.scrapper_settings.DATASOFT_SELECTORS["INSTALLMENTS"])
            n_instalments = [int(n) for n in re.findall(r"\d+", installments.text)]
            installments_options = {}
            for i, inst in enumerate(n_instalments):
                installments_options[f"option {i+1}"] = f"{inst} cuotas"
            
            self.product_data["name"] = product_title.text if product_title else ""
            self.product_data["sku"] = sku.text if sku else ""
            self.product_data["brand"] = brand.text if brand else ""
            self.product_data["main_category"] = category_path[1].text if len(category_path)>1 else ""
            self.product_data["sub_category"] = category_path[2].text if len(category_path)>2 else ""
            self.product_data["list_price"] = list_price.text.replace(".", "") if list_price else ""
            self.product_data["cash_price"] = cash_price.text.replace("$", "").replace(".", "") if cash_price else ""
            self.product_data["discount_applicated"] = round(discount_applicated, 2)
            self.product_data["installments"] = installments_options
            self.product_data["stock"] = "Available"
            self.product_data["warranty"] = ""
            self.product_data["store"] = "Datasoft"
            self.product_data["link"] = self.link
            logging.info(f"------------PRODUCT DATA------------>{self.product_data}")
            logging.info(
                "---------------------------------------------------------------------------------------------------"
            )
            logging.info("")
            logging.info("")
            return self.product_data
        
        elif "armytech.com.ar" in self.link:
            logging.info(
                    "---------------------------------------------------------------------------------------------------"
                )
            logging.info(f"ACCEDIENDO A {self.link}")
            logging.info(self.driver)
            self.driver.get(self.link)
            time.sleep(random.uniform(2, 5))

            product_title = self.extract_elements.safe_find_elements(By.XPATH, self.scrapper_settings.ARMYTECH_SELECTORS["PRODUCT_TITLE"])
            sku = self.extract_elements.safe_find_elements(By.XPATH, self.scrapper_settings.ARMYTECH_SELECTORS["SKU"])
            brand_a = self.extract_elements.safe_find_elements(By.XPATH, self.scrapper_settings.ARMYTECH_SELECTORS["BRAND"])
            brand_link = brand_a.get_attribute("href")
            parsed = urlparse(brand_link)
            path = parsed.path 
            brand = path.rstrip("/").split("/")[-1]
            logging.info(f"BRAND LINK -------> {brand}")
            product_link_parsed = urlparse(self.link)
            product_link_path = product_link_parsed.path
            category_path = product_link_path.rstrip("/").split("/")[-2]
            logging.info(f"PRODUCT CATEGORY -------> {category_path}")
            list_price = self.extract_elements.safe_find_elements(By.XPATH, self.scrapper_settings.ARMYTECH_SELECTORS["LIST_PRICE"])
            cash_price = self.extract_elements.safe_find_elements(By.XPATH, self.scrapper_settings.ARMYTECH_SELECTORS["CASH_PRICE"])
            logging.info(f"LIST PRICE -------> {list_price.text}, CASH PRICE -------> {cash_price.text}")
            discount_applicated = 100 - ((float(cash_price.text.replace("$ ", "").replace(".", "").replace(",", "."))/float(list_price.text.replace("Precio de Lista $ ", ""))) * 100)
            logging.info(f"DISCOUNT APPLICATED -------> {round(discount_applicated, 2)}")
            installments = self.extract_elements.safe_find_elements(By.XPATH, self.scrapper_settings.ARMYTECH_SELECTORS["INSTALLMENTS"], multiple=True)
            installments_text = [inst.text for inst in installments if "cuotas" in inst.text]
            logging.info(f"PRODUCTS INSTALMENTS ----> {installments_text}")
            installments_options = {}
            for i, inst in enumerate(installments_text):
                installments_options[f"option {i+1}"] = inst

            self.product_data["name"] = product_title.text if product_title else ""
            self.product_data["sku"] = sku.text if sku else ""
            self.product_data["brand"] = brand
            if "procesador" in category_path or "memorias" in category_path:
                self.product_data["main_category"] = "hardware"
            self.product_data["sub_category"] = category_path
            self.product_data["list_price"] = list_price.text.replace("Precio de Lista $ ", "") if list_price else ""
            self.product_data["cash_price"] = cash_price.text.replace("$ ", "").replace(".", "").replace(",", ".") if cash_price else ""
            self.product_data["discount_applicated"] = round(discount_applicated, 2)
            self.product_data["installments"] = installments_options
            self.product_data["stock"] = "Available"
            self.product_data["warranty"] = ""
            self.product_data["store"] = "Army Tech"
            self.product_data["link"] = self.link
            logging.info(f"------------PRODUCT DATA------------>{self.product_data}")
            logging.info(
                "---------------------------------------------------------------------------------------------------"
            )
            logging.info("")
            logging.info("")
            return self.product_data
        
        elif "compragamer.com" in self.link:
            logging.info(
                    "---------------------------------------------------------------------------------------------------"
                )
            logging.info(f"ACCEDIENDO A {self.link}")
            logging.info(self.driver)
            self.driver.get(self.link)
            time.sleep(random.uniform(2, 5))

            product_title = self.extract_elements.safe_find_elements(By.XPATH, self.scrapper_settings.COMPRA_GAMER_SELECTORS["PRODUCT_TITLE"])
            sku = self.extract_elements.safe_find_elements(By.XPATH, self.scrapper_settings.COMPRA_GAMER_SELECTORS["SKU"])
            brand = self.extract_elements.safe_find_elements(By.XPATH, self.scrapper_settings.COMPRA_GAMER_SELECTORS["BRAND"])
            category_path = self.extract_elements.safe_find_elements(By.XPATH, self.scrapper_settings.COMPRA_GAMER_SELECTORS["CATEGORY_PATH"], multiple=True)
            category = [cat.text.split(" > ")[0] for cat in category_path]
            logging.info(f"PRODUCT CATEGORY -------> {category}")
            list_price = self.extract_elements.safe_find_elements(By.XPATH, self.scrapper_settings.COMPRA_GAMER_SELECTORS["LIST_PRICE"])
            cash_price = self.extract_elements.safe_find_elements(By.XPATH, self.scrapper_settings.COMPRA_GAMER_SELECTORS["CASH_PRICE"])
            logging.info(f"LIST PRICE -------> {list_price.text}, CASH PRICE -------> {cash_price.text}")
            discount_applicated = 100 - ((float(cash_price.text.replace(".", ""))/float(list_price.text.replace(".", ""))) * 100)
            installments_options = {}
            installments = [i for i in range(1, 7) if i == 1 or i % 3 == 0]
            logging.info(f'PRODUCT INSTALMENTS ----> {installments}')
            for i, inst in enumerate(installments):
                installments_options[f"option {i+1}"] = f"{inst} cuotas sin interes"
            stock = self.extract_elements.safe_find_elements(By.XPATH, self.scrapper_settings.COMPRA_GAMER_SELECTORS["STOCK"])
            warranty = self.extract_elements.safe_find_elements(By.XPATH, self.scrapper_settings.COMPRA_GAMER_SELECTORS["WARRANTY"])

            self.product_data["name"] = product_title.text if product_title else ""
            self.product_data["sku"] = sku.text if sku else ""
            self.product_data["brand"] = brand.text if brand else ""
            if "procesador" in category[0] or "Procesador" in category[0] or "Memorias" in category[0] or "memorias" in category[0]:
                self.product_data["main_category"] = "hardware"
            self.product_data["main_category"] = "Other"
            self.product_data["sub_category"] = category[0]
            self.product_data["list_price"] = list_price.text.replace(".", "") if list_price else ""
            self.product_data["cash_price"] = cash_price.text.replace(".", "") if cash_price else ""
            self.product_data["discount_applicated"] = round(discount_applicated, 2)
            self.product_data["installments"] = installments_options
            self.product_data["stock"] = "Available" if "disponible" in stock.text else "Not available"
            self.product_data["warranty"] = warranty.text if warranty else ""
            self.product_data["store"] = "Compra Gamer"
            self.product_data["link"] = self.link
            logging.info(f"------------PRODUCT DATA------------>{self.product_data}")
            logging.info(
                "---------------------------------------------------------------------------------------------------"
            )
            logging.info("")
            logging.info("")
            return self.product_data