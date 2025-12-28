from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.config.settings import Settings

class ExtractElements:
    def __init__(self, __driver__):
        self.settings = Settings()
        self.driver = __driver__

    def safe_find_elements(self, by, path, multiple=False, index=0, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout)
            if multiple:
                print("MULTIPLE")
                wait.until(EC.presence_of_all_elements_located((by, path)))
                elements = self.driver.find_elements(by, path)
                return elements if elements else []
            else:
                print("ELEMENT")
                wait.until(EC.presence_of_element_located((by, path)))
                element = self.driver.find_element(by, path)
                return element if element else None
        except Exception as e:
            print("Fallo al obtener el texto:", e)
            return None
