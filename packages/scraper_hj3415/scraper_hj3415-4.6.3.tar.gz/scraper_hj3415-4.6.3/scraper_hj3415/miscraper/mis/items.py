# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MisItems(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    value = scrapy.Field()
