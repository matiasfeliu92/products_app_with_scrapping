import logging
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class Settings:
    def __init__(self):
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        self.MEXX_SELECTORS = {
            "PRODUCT_TITLE": "h1",
            "SKU": "#prod_desc_edit > div.row.pr-0.pl-0.filaMarcas > div > h6:nth-child(2)",
            "BRAND": "body > div.section.single.ecommerce-page.mt-0.pt-0 > div > div > div:nth-child(9) > div:nth-child(3) > span:nth-child(1) > p",
            "CATEGORY_PATH": "div.col-md-12.pt-2.pb-2 > ul.breadcrum.nav.navbar-nav.navbar-left",
            "LIST_PRICE": "#precio > span > b.mr-2.ft-3.PRECIO_NEW",
            "CASH_PRICE": "#prod_desc_edit > h2 > b:nth-child(2)",
            "INSTALLMENTS": "#precio > span > b.anterior_single.preciobot2",
            "STOCK": "#prod_desc_edit > div:nth-child(3) > h6 > div",
            "WARRANTY": "div.garantia-bloque p"
        }
        self.FULLH4RD_SELECTORS = {
            "PRODUCT_TITLE": "h1",
            "SKU": "p.codebar",
            "BRAND": "",
            "CATEGORY_PATH": 'a > span[itemprop="item"] > span[itemprop="name"]',
            "INSTALLMENTS": "div.price-special-container > p",
            "LIST_PRICE": "",
            "CASH_PRICE": "div.price-list-container > p > span.bold",
            "DISCOUNT_APPLICATED": "div.price-list-container > p:nth-child(1) > span:nth-child(2)",
            "WEB_STOCK": "div.stock-container > div:nth-child(1) > h5",
            "LOCAL_STOCK": "div.stock-container > div:nth-child(2) > h5",
            "WARRANTY": "//li[contains(text(), 'Garantía')]"
        }
        self.DATASOFT_SELECTORS = {
            "PRODUCT_TITLE": "h1 > span",
            "SKU": 'span[itemprop="sku"]',
            "BRAND": 'div.short_desc > ul > li:nth-child(1)',
            "CATEGORY_PATH": 'div.col-xs-12 > ul.breadcrumb > li > span > a[itemprop="url"] > span[itemprop="title"]',
            "INSTALLMENTS": "div.block.pago > div:nth-child(1) > span",
            "LIST_PRICE": "span.pesos > strong",
            "CASH_PRICE": "#final_price",
            "DISCOUNT_APPLICATED": "",
            "WARRANTY": "//td[contains(text(), 'Garantía')]/following-sibling::td"
        }


    def get_chrome_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(f"--user-agent={self.USER_AGENT}")

        if platform.system() == "Windows":
            service = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=options)

        options.binary_location = "/usr/bin/chromium"
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service("/usr/bin/chromedriver")
        return webdriver.Chrome(service=service, options=options)