from logging import WARNING
from functools import cache

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log

from utils.logger import logger
from utils.settings import settings

_retry = retry(
    retry=retry_if_exception_type(TimeoutException),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    before_sleep=before_sleep_log(logger, WARNING),
    reraise=True,
)

_TABLE_XPATH = "//div[@data-testid='screener-table']//table"
_NEXT_BUTTON_XPATH = "//button[@data-testid='next-page-button']"
_REGION_FILTER_XPATH = "//button[contains(@class,'menuBtn') and .//div[normalize-space(text())='Region']]"
_REGION_OPTION_XPATH = "//span[text()='{region}']"
_REGION_APPLY_XPATH = "//button[normalize-space()='Apply']"


@cache
class Scraper:
    """Headless Chrome scraper for the Yahoo Finance equity screener."""

    def __init__(self, region):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = settings.URL
        self.region = region

    def _navigate(self):
        """Loads the screener URL and waits for the table to be present."""
        logger.info("Navigating to %s", self.url)
        self.driver.get(self.url)
        self.wait.until(EC.presence_of_element_located((By.XPATH, _TABLE_XPATH)))
        logger.debug("Page loaded and table found")

    @_retry
    def _get_table_page(self) -> str:
        """Returns the outerHTML of the screener table."""
        logger.debug("Waiting for table to be visible")
        table = self.wait.until(
            EC.presence_of_element_located((By.XPATH, _TABLE_XPATH))
        )
        return table.get_attribute("outerHTML")

    @_retry
    def _apply_filter(self):
        """Opens the region filter, selects the configured region and applies it."""
        logger.info("Applying region filter: %s", self.region)
        region_filter = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, _REGION_FILTER_XPATH))
        )
        self.driver.execute_script("arguments[0].click();", region_filter)

        option_xpath = _REGION_OPTION_XPATH.format(region=self.region)
        option = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )
        option.click()

        apply_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, _REGION_APPLY_XPATH))
        )
        apply_button.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, _TABLE_XPATH)))
        logger.debug("Region filter applied")

    def next_table_page(self) -> bool:
        """Clicks the next page button."""
        try:
            button = self.driver.find_element(By.XPATH, _NEXT_BUTTON_XPATH)

            if not button.is_enabled():
                logger.info("Next page button is disabled — last page reached")
                return False

            button.click()
            return True

        except NoSuchElementException:
            logger.error("Next button not found")
            raise

    def get_all_table_pages(self) -> list[str]:
        logger.info("Starting full table scrape")
        all_data = []
        page = 2
        try:
            self._navigate()
            self._apply_filter()
            all_data.append(self._get_table_page())
            while self.next_table_page():
                all_data.append(self._get_table_page())
                logger.debug("%s pages collected", page)
                page += 1
        finally:
            logger.info("Finished extraction, %s pages collected", page - 1)
            self.driver.quit()
        return all_data
