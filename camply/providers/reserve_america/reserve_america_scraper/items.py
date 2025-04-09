# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CampgroundAvailabilityItem(scrapy.Item):
    parkId = scrapy.Field()
    site = scrapy.Field()
    date = scrapy.Field()
    availability = scrapy.Field()
