import scrapy
from scrapy import Request
from scrapy.http import Response

from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def init_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )
    return driver


class DouSpider(scrapy.Spider):
    name = 'dou'
    allowed_domains = ["jobs.dou.ua"]
    start_urls = ["https://jobs.dou.ua/vacancies/?category=Python"]

    def parse(self, response: Response) -> Request:
        pass


    @classmethod
    def load_all_page(cls, driver: webdriver.Chrome) -> None:
        while True:
            try:
                more_button = WebDriverWait(driver, 2).until(
                    ec.presence_of_element_located(
                        (By.CLASS_NAME, "more-btn")
                    )
                )

                if (
                        "disabled" not in more_button.get_attribute("class")
                        and more_button.is_displayed()
                ):
                    more_button.click()
                    print("Clicked 'More' button")
                else:
                    print("'More' button is either disabled or not displayed")
                    break
            except (NoSuchElementException, ElementNotInteractableException) as e:
                print("The 'More' button was not found or became unavailable:", e)
                break
