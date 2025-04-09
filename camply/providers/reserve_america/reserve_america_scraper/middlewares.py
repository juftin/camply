# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import logging
import time
from datetime import datetime, timedelta

# useful for handling different item types with a single interface
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from camply.containers.data_containers import AvailableCampsite

logger = logging.getLogger(__name__)

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


class CamplyReserveAmericaSpiderMiddleware:
    """
    Spider middleware to convert scraped items (raw availability) into
    `AvailableCampsite` objects. Accumulates them so they can be retrieved
    by the spider or provider at the end of the crawl.
    """

    def __init__(self):
        # Store processed campsite objects here
        self.available_campsites = []

    @classmethod
    def from_crawler(cls, crawler):
        """
        Create the middleware and connect signals.
        """
        middleware = cls()
        # Connect signals
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        logger.debug(f"Spider opened: {spider.name}")

    def item_scraped(self, item, spider):
        """
        Convert the scraped item (if it's available) into an `AvailableCampsite`,
        then store it in `self.available_campsites`.
        """
        availability = item.get("availability", "").lower()

        # Only process items that are actually "Available"
        if availability == "a":
            # For example, parse the date from the item
            date_str = item["date"]  # e.g. '2025-04-01'
            booking_date = datetime.strptime(date_str, "%Y-%m-%d")
            # Create your `AvailableCampsite` object
            campsite = AvailableCampsite(
                campsite_id=item["site"],
                booking_date=booking_date,
                booking_end_date=booking_date + timedelta(days=1),
                booking_nights=1,
                campsite_site_name=str(item["site"]),
                campsite_loop_name="Placeholder Loop Name",
                # TODO: Replace with actual loop name
                campsite_occupancy=[1, 1],
                # TODO: Replace with actual occupancy
                availability_status=item["availability"],
                recreation_area="Placeholder Recreation Area",
                # TODO: Replace with actual Recreation Area name
                recreation_area_id=item["parkId"],
                facility_name="Placeholder Facility Name",
                # TODO: Replace with actual Facility name
                facility_id=item["parkId"],
                booking_url="placeholder.url",
                # TODO: Replace with actual booking URL
            )
            self.available_campsites.append(campsite)

    def spider_closed(self, spider, reason):
        """
        When the spider finishes, optionally store the list of available_campsites
        back onto the spider so the provider can retrieve them.
        """
        spider.logger.info(f"Spider closed: {spider.name}, reason: {reason}")
        spider.available_campsites = self.available_campsites


class HumanInTheDownloaderMiddleware:
    def __init__(self):
        self.driver = self.create_headful_driver()
        # TODO: Only use the headful if a captcha is detected.
        #   [ ] Save session (cookies) that can be passed between headless and headful drivers
        #   [ ] Write headless driver
        #   [ ] Detect if captcha is present and switch to headful driver
        #   [ ] Switch back to headless driver after captcha is solved
        #   [ ] Save session (cookies) to configuration file

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
