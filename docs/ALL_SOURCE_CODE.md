docs/ALL_SOURCE_CODE.md  # Complete Source Code

Run setup_framework.py OR copy code below:

## pages/base_page.py
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config.config import config
import allure

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)
    
    @allure.step("Click: {locator}")
    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
    
    @allure.step("Type: {text}")
    def send_keys(self, locator, text):
        el = self.wait.until(EC.presence_of_element_located(locator))
        el.clear()
        el.send_keys(text)
    
    def get_text(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator)).text
```

## api/base_api.py
```python
import requests
from config.config import config
import allure

class BaseAPI:
    def __init__(self):
        self.base_url = config.API_BASE_URL
        self.session = requests.Session()
    
    @allure.step("GET {endpoint}")
    def get(self, endpoint, **kwargs):
        return self.session.get(f"{self.base_url}/{endpoint}", **kwargs)
    
    @allure.step("POST {endpoint}")
    def post(self, endpoint, **kwargs):
        return self.session.post(f"{self.base_url}/{endpoint}", **kwargs)
```

## tests/web/test_saucedemo.py
```python
import pytest
import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

@allure.feature("Web Testing")
@pytest.mark.ui
@pytest.mark.smoke
class TestSauceDemo:
    
    @allure.story("Login")
    def test_login(self, driver):
        page = BasePage(driver)
        driver.get("https://www.saucedemo.com")
        page.send_keys((By.ID, "user-name"), "standard_user")
        page.send_keys((By.ID, "password"), "secret_sauce")
        page.click((By.ID, "login-button"))
        assert "inventory" in driver.current_url
```

## tests/api/test_restful_booker.py
```python
import pytest
import allure
from api.base_api import BaseAPI

@allure.feature("API Testing")
@pytest.mark.api
@pytest.mark.regression
class TestRestfulBooker:
    
    @allure.story("Get Bookings")
    def test_get_bookings(self):
        api = BaseAPI()
        api.base_url = "https://restful-booker.herokuapp.com"
        response = api.get("booking")
        assert response.status_code == 200
        assert len(response.json()) > 0
```

## utils/logger.py
```python
import logging
import coloredlogs

def get_logger(name):
    logger = logging.getLogger(name)
    coloredlogs.install(level='INFO', logger=logger)
    return logger
```

Repository: https://github.com/YuvarajNeelagandan/pytest-automation-framework
Run: python setup_framework.py
