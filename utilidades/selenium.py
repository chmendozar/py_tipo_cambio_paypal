import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger("Utils - Selenium")
logging.basicConfig(level=logging.INFO)

class SeleniumHelper:
    def __init__(self, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        logger.info("Initialized Selenium WebDriver with webdriver-manager.")

    def open_url(self, url):
        """Open a URL in the browser."""
        logger.info(f"Opening URL: {url}")
        self.driver.get(url)

    def find_element(self, by, value, timeout=10):
        """Find an element on the page."""
        logger.info(f"Finding element by {by} with value '{value}' (timeout={timeout}s).")
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            logger.info(f"Element found: {value}")
            return element
        except TimeoutException:
            logger.error(f"Element not found: {value}")
            return None

    def click_element(self, by, value, timeout=10):
        """Click an element on the page."""
        logger.info(f"Attempting to click element by {by} with value '{value}'.")
        element = self.find_element(by, value, timeout)
        if element:
            element.click()
            logger.info(f"Clicked element: {value}")

    def send_keys(self, by, value, keys, timeout=10):
        """Send keys to an input element."""
        logger.info(f"Sending keys to element by {by} with value '{value}'.")
        element = self.find_element(by, value, timeout)
        if element:
            element.send_keys(keys)
            logger.info(f"Keys sent to element: {value}")

    def get_text(self, by, value, timeout=10):
        """Get text from an element."""
        logger.info(f"Getting text from element by {by} with value '{value}'.")
        element = self.find_element(by, value, timeout)
        if element:
            text = element.text
            logger.info(f"Text retrieved: {text}")
            return text
        logger.warning(f"Failed to retrieve text from element: {value}")
        return None

    def close_browser(self):
        """Close the browser."""
        logger.info("Closing the browser.")
        self.driver.quit()