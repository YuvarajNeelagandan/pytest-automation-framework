from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """
    Base Page class that all page objects inherit from.
    Contains common methods for interacting with web elements.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)
        logger.info(f"Initialized {self.__class__.__name__}")

    @allure.step("Navigate to {url}")
    def navigate_to(self, url):
        """
        Navigate to a URL.
        """
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)

    @allure.step("Find element {locator}")
    def find_element(self, locator, timeout=10):
        """
        Find a single element with explicit wait.
        """
        try:
            logger.debug(f"Finding element: {locator}")
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise

    @allure.step("Find elements {locator}")
    def find_elements(self, locator, timeout=10):
        """
        Find multiple elements with explicit wait.
        """
        try:
            logger.debug(f"Finding elements: {locator}")
            wait = WebDriverWait(self.driver, timeout)
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            logger.error(f"Elements not found: {locator}")
            raise

    @allure.step("Click element {locator}")
    def click(self, locator, timeout=10):
        """
        Click on an element.
        """
        try:
            logger.info(f"Clicking element: {locator}")
            element = self.wait_for_clickable(locator, timeout)
            element.click()
        except Exception as e:
            logger.error(f"Failed to click element {locator}: {str(e)}")
            raise

    @allure.step("Enter text '{text}' into {locator}")
    def enter_text(self, locator, text, timeout=10):
        """
        Clear and enter text into an element.
        """
        try:
            logger.info(f"Entering text into {locator}")
            element = self.find_element(locator, timeout)
            element.clear()
            element.send_keys(text)
        except Exception as e:
            logger.error(f"Failed to enter text into {locator}: {str(e)}")
            raise

    @allure.step("Get text from {locator}")
    def get_text(self, locator, timeout=10):
        """
        Get text from an element.
        """
        try:
            logger.debug(f"Getting text from: {locator}")
            element = self.find_element(locator, timeout)
            text = element.text
            logger.debug(f"Text retrieved: {text}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from {locator}: {str(e)}")
            raise

    def get_attribute(self, locator, attribute, timeout=10):
        """
        Get attribute value from an element.
        """
        try:
            logger.debug(f"Getting attribute '{attribute}' from: {locator}")
            element = self.find_element(locator, timeout)
            value = element.get_attribute(attribute)
            return value
        except Exception as e:
            logger.error(f"Failed to get attribute from {locator}: {str(e)}")
            raise

    def wait_for_visible(self, locator, timeout=10):
        """
        Wait for element to be visible.
        """
        try:
            logger.debug(f"Waiting for element to be visible: {locator}")
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.visibility_of_element_located(locator))
            return element
        except TimeoutException:
            logger.error(f"Element not visible: {locator}")
            raise

    def wait_for_clickable(self, locator, timeout=10):
        """
        Wait for element to be clickable.
        """
        try:
            logger.debug(f"Waiting for element to be clickable: {locator}")
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            logger.error(f"Element not clickable: {locator}")
            raise

    def is_element_present(self, locator, timeout=5):
        """
        Check if element is present on the page.
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_visible(self, locator, timeout=5):
        """
        Check if element is visible on the page.
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def scroll_to_element(self, locator):
        """
        Scroll to an element.
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def hover_over(self, locator):
        """
        Hover over an element.
        """
        element = self.find_element(locator)
        self.actions.move_to_element(element).perform()

    def get_current_url(self):
        """
        Get the current URL.
        """
        return self.driver.current_url

    def get_title(self):
        """
        Get the page title.
        """
        return self.driver.title

    @allure.step("Take screenshot")
    def take_screenshot(self, name="screenshot"):
        """
        Take a screenshot and attach to Allure report.
        """
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
