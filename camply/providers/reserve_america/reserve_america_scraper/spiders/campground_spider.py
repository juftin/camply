import time
from datetime import datetime, timedelta
from urllib.parse import parse_qs, urlparse

import scrapy
from reserve_america_scraper.items import CampgroundAvailabilityItem
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


class CampgroundSpider(scrapy.Spider):
    name = "campground"
    allowed_domains = [
        "massdcrcamping.reserveamerica.com",
        "go.aspiraconnect.com",
    ]

    def __init__(
        self, start_date=None, end_date=None, park_id="32608", *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        # Default start_date is today, default end_date is 6 weeks from start_date.
        if start_date is None:
            start_date = datetime.today().strftime("%m/%d/%Y")
        self.start_date_str = start_date
        self.start_date = datetime.strptime(start_date, "%m/%d/%Y").date()

        if end_date is None:
            end_date = (self.start_date + timedelta(weeks=6)).strftime("%m/%d/%Y")
        self.end_date_str = end_date
        self.end_date = datetime.strptime(end_date, "%m/%d/%Y").date()

        self.park_id = park_id

    def start_requests(self):
        # Update the URL to include the start_date instead of "null"
        start_urls = [
            f"https://massdcrcamping.reserveamerica.com/campsiteCalendar.do?page=calendar&contractCode=MA&parkId={self.park_id}&calarvdate={self.start_date_str}&sitepage=true&startIdx=0",
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={"selenium": True})

    def parse(self, response):
        # Process the current date window's data.
        yield from self.parse_page(response)
        # Scrape all pages in the current date window by navigating appropriately.
        yield from self.scrape_all_pages_in_date_window(response)
        # Finally, handle the "Next 2 Weeks" date pagination.
        yield from self.paginate_date_window(response)

    def parse_page(self, response):
        """
        Extract header information (month/year and day numbers) and process each campsite row,
        yielding an item for each site's availability.
        """
        daterange_div = response.css("#daterangediv")
        if not daterange_div:
            self.logger.warning("No daterangediv found in response")
            with open("no_daterangediv_response.html", "wb") as f:
                f.write("No daterangediv found in response".encode())
                f.write(response.body)
            yield scrapy.Request(response.url, meta={"selenium": True})
            return

        # Extract month and year
        month, year = self._extract_month_year(daterange_div)

        # Extract dates
        dates = self._extract_dates(daterange_div, month, year)

        # Process campsite rows
        yield from self._process_campsite_rows(daterange_div, dates, response)

    def _extract_month_year(self, daterange_div):
        """
        Extract the month and year from the daterange_div.
        """
        month_text = daterange_div.css(
            "div.empty.top.rght .td.weeknav.month span::text"
        ).get()
        if month_text:
            try:
                dt = datetime.strptime(month_text.strip(), "%b %Y")
                return dt.month, dt.year
            except Exception as e:
                self.logger.error(f"Error parsing month/year from '{month_text}': {e}")
        return datetime.now().month, datetime.now().year

    def _extract_dates(self, daterange_div, month, year):
        """
        Extract header cells for the day numbers and return a list of dates.
        """
        header_cells = daterange_div.css("#calendar .thead div.th.calendar")
        dates = []
        for cell in header_cells:
            day_text = cell.css("div.date::text").get()
            if day_text:
                try:
                    day = int(day_text.strip())
                    date_obj = datetime(year, month, day).date()
                    dates.append(date_obj)
                except Exception as e:
                    self.logger.error(f"Error parsing day '{day_text}': {e}")
                    dates.append(None)
            else:
                dates.append(None)
        self.logger.info(f"Extracted dates: {dates}")
        return dates

    def _process_campsite_rows(self, daterange_div, dates, response):
        """
        Process each campsite row and yield items for each site's availability.
        """
        rows = daterange_div.css("#calendar > div.br")
        self.logger.info(f"Found {len(rows)} site rows")
        qs = parse_qs(urlparse(response.url).query)
        parkId = qs.get("parkId", [None])[0]

        for row in rows:
            site = row.css("div.td.sn .siteListLabel a::text").get()
            site = site.strip() if site else ""
            availability_cells = row.css("div.td.status")
            if len(availability_cells) != len(dates):
                self.logger.warning(
                    f"Row with site {site}: number of availability cells ({len(availability_cells)}) does not match number of dates ({len(dates)})"
                )
            for i, cell in enumerate(availability_cells):
                if i < len(dates) and dates[i]:
                    avail = cell.css("::text").get()
                    avail = avail.strip() if avail else ""
                    item = CampgroundAvailabilityItem()
                    item["parkId"] = parkId
                    item["site"] = site
                    item["date"] = dates[i].isoformat()
                    item["availability"] = avail
                    yield item

    def scrape_all_pages_in_date_window(self, response):
        """
        Check for the presence of next and previous pagination buttons.
        - If next exists and previous does not, assume the page is the first page and navigate forward.
        - If previous exists and next does not, assume the page is the last page and navigate backward.
        - If both exist, raise an error.
        """
        daterange_div = response.css("#daterangediv")
        next_page_href = daterange_div.css(
            "span.pagenav a#resultNext_dr_top::attr(href)"
        ).get()
        prev_page_href = daterange_div.css(
            "span.pagenav a#resultPrevious_dr_top::attr(href)"
        ).get()

        if next_page_href and not prev_page_href:
            self.logger.info("Detected first page of date window; navigating forward.")
            yield from self.scrape_pages_forward(response)
        elif prev_page_href and not next_page_href:
            self.logger.info("Detected last page of date window; navigating backward.")
            yield from self.scrape_pages_backward(response)
        elif next_page_href and prev_page_href:
            self.logger.error(
                "Both next and previous pagination buttons exist. Ambiguous starting page."
            )
            raise ValueError(
                "Both next and previous pagination buttons exist. Cannot determine starting page."
            )
        else:
            self.logger.info("No pagination buttons found; single page date window.")

    def scrape_pages_forward(self, response):
        """
        If on the first page, repeatedly click the next-page button to scrape forward
        until no next-page button is found.
        """
        driver = response.request.meta.get("driver")
        if not driver:
            self.logger.error("No Selenium driver found in response meta!")
            return

        while True:
            try:
                next_button = driver.find_element(
                    By.CSS_SELECTOR, "a#resultNext_dr_top"
                )
                if not next_button.is_displayed() or not next_button.is_enabled():
                    self.logger.info("Next button not clickable; reached last page.")
                    break
            except Exception:
                self.logger.info("No next page button found; reached last page.")
                break

            self.logger.info("Clicking next page button via Selenium.")
            try:
                actions = ActionChains(driver)
                actions.move_to_element(next_button).click().perform()
                time.sleep(3)  # Consider using WebDriverWait for a more robust wait.
                new_page = driver.page_source
                new_url = driver.current_url
                new_response = scrapy.http.HtmlResponse(
                    url=new_url,
                    body=new_page,
                    encoding="utf-8",
                    request=response.request,
                )
                yield from self.parse_page(new_response)
                # Check if there's another next page.
                daterange_div = new_response.css("#daterangediv")
                next_page_href = daterange_div.css(
                    "span.pagenav a#resultNext_dr_top::attr(href)"
                ).get()
                if not next_page_href:
                    self.logger.info("No further next page found; reached last page.")
                    break
            except Exception as e:
                self.logger.error(f"Error clicking next page: {e}")
                break

    def scrape_pages_backward(self, response):
        """
        If on the last page, repeatedly click the previous-page button to scrape backward
        until no previous-page button is found (i.e. reached the first page).
        """
        driver = response.request.meta.get("driver")
        if not driver:
            self.logger.error("No Selenium driver found in response meta!")
            return

        while True:
            try:
                prev_button = driver.find_element(
                    By.CSS_SELECTOR, "a#resultPrevious_dr_top"
                )
                if not prev_button.is_displayed() or not prev_button.is_enabled():
                    self.logger.info(
                        "Previous button not clickable; reached first page."
                    )
                    break
            except Exception:
                self.logger.info("No previous page button found; reached first page.")
                break

            self.logger.info("Clicking previous page button via Selenium.")
            try:
                actions = ActionChains(driver)
                actions.move_to_element(prev_button).click().perform()
                time.sleep(3)
                new_page = driver.page_source
                new_url = driver.current_url
                new_response = scrapy.http.HtmlResponse(
                    url=new_url,
                    body=new_page,
                    encoding="utf-8",
                    request=response.request,
                )
                yield from self.parse_page(new_response)
                # Check if there's another previous page.
                daterange_div = new_response.css("#daterangediv")
                prev_page_href = daterange_div.css(
                    "span.pagenav a#resultPrevious_dr_top::attr(href)"
                ).get()
                if not prev_page_href:
                    self.logger.info(
                        "No further previous page found; reached first page."
                    )
                    break
            except Exception as e:
                self.logger.error(f"Error clicking previous page: {e}")
                break

    def paginate_date_window(self, response):
        """
        Handle date pagination ("Next 2 Weeks") using Selenium.
        Click the Next 2 Weeks button if it exists and if the target date is within the allowed range.
        """
        daterange_div = response.css("#daterangediv")
        next_week_href = daterange_div.css(
            "div.empty.top.rght a#nextWeek::attr(href)"
        ).get()
        if next_week_href:
            parsed_url = urlparse(next_week_href)
            params = parse_qs(parsed_url.query)
            calarvdate_str = params.get("calarvdate", [None])[0]
            if calarvdate_str:
                try:
                    next_window_date = datetime.strptime(
                        calarvdate_str, "%m/%d/%Y"
                    ).date()
                    if next_window_date > self.end_date:
                        self.logger.info(
                            "Reached beyond end_date; stopping date pagination."
                        )
                        return
                except Exception as e:
                    self.logger.error(
                        f"Error parsing calarvdate '{calarvdate_str}': {e}"
                    )
            try:
                driver = response.request.meta.get("driver")
                if not driver:
                    self.logger.error("No Selenium driver found in response meta!")
                    return
                next_week_button = driver.find_element(
                    By.CSS_SELECTOR, "div.empty.top.rght a#nextWeek"
                )
                self.logger.info("Clicking Next 2 Weeks button via Selenium.")
                actions = ActionChains(driver)
                actions.move_to_element(next_week_button).click().perform()
                time.sleep(3)
                new_page = driver.page_source
                new_url = driver.current_url
                new_response = scrapy.http.HtmlResponse(
                    url=new_url,
                    body=new_page,
                    encoding="utf-8",
                    request=response.request,
                )
                yield from self.parse(new_response)
            except Exception as e:
                self.logger.error(f"Error during date pagination: {e}")
        else:
            self.logger.info("No further date pagination found.")
