import time

import scrapy
from scrapy import Request
from scrapy.http import Response
from selenium import webdriver
from selenium.common import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from dou.config import TECHNOLOGIES
from dou.items import DouItem


class DouSpider(scrapy.Spider):
    name = "dou"
    allowed_domains = ["jobs.dou.ua"]
    start_urls = ["https://jobs.dou.ua/vacancies/?category=Python"]

    def init_driver(self) -> webdriver.Chrome:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
        return driver

    def parse(self, response: Response, **kwargs) -> Request:
        driver = self.init_driver()
        driver.get(response.url)
        self._load_all_page(driver)
        html_source = driver.page_source
        driver.quit()
        response = response.replace(body=html_source)

        for vacancy in response.css(".l-vacancy"):
            vacancy_url = vacancy.css(".title .vt::attr(href)").get()
            if vacancy_url:
                yield response.follow(vacancy_url, callback=self.parse_detail_page)

    @classmethod
    def _load_all_page(cls, driver: webdriver.Chrome) -> None:
        click_count = 0
        while True:
            try:
                more_button = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, ".more-btn a"))
                )

                driver.execute_script("arguments[0].scrollIntoView(true);", more_button)

                if (
                    more_button.is_displayed()
                    and "disabled" not in more_button.get_attribute("class")
                ):
                    more_button.click()
                    click_count += 1
                    print(f"Clicked 'More' button {click_count} times")

                    time.sleep(2)

                else:
                    print("'More' button is either disabled or not displayed")
                    break

            except (
                NoSuchElementException,
                ElementNotInteractableException,
                TimeoutException,
            ) as e:
                print(f"The 'More' button was not found or became unavailable: {e}")
                break

    def parse_detail_page(self, response: Response) -> dict:
        item = DouItem()

        item["title"] = response.css(".b-vacancy h1::text").get().strip()
        item["company"] = response.css("div.l-n a::text").get().strip()

        salary = response.css("span.salary::text").get()
        item["salary"] = salary.strip() if salary else "Not specified"

        description = " ".join(
            response.css("div.b-typo.vacancy-section ::text").getall()
        ).strip()
        item["description"] = description if description else "No description available"

        item["technologies"] = [
            technology
            for technology in TECHNOLOGIES
            if technology.lower() in description.lower()
        ]

        yield item
