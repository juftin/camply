# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import logging
import time

# useful for handling different item types with a single interface
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.INFO)


class ReserveAmericaScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it does not have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class HumanInTheDownloaderMiddleware:
    def __init__(self):
        self.driver = self.create_headful_driver()

    def create_headful_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def process_request(self, request, spider):
        # Process only requests marked with meta['selenium'].
        if not request.meta.get("selenium"):
            return None

        self.driver.get(request.url)
        time.sleep(3)  # Wait for JavaScript elements to load.
        body = self.driver.page_source

        # Check for a captcha. Adjust this check as needed.
        if "captcha" in body.lower():
            spider.logger.info("Captcha detected!")
            spider.logger.info(
                "Please solve the captcha in the browser window, then press Enter to continue..."
            )
            input("Press Enter after solving the captcha...")
            body = self.driver.page_source

        # Attach the Selenium driver to the request meta so it's available later.
        request.meta["driver"] = self.driver

        return HtmlResponse(
            url=self.driver.current_url, body=body, encoding="utf-8", request=request
        )

    def process_response(self, request, response, spider):
        # Return the response unmodified.
        return response

    def process_exception(self, request, exception, spider):
        spider.logger.error(f"Exception in HumanInTheMiddleware: {exception}")

    def spider_closed(self, spider):
        self.driver.quit()
