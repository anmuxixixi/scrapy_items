# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SuningbookItem(scrapy.Item):
    # define the fields for your item here like:
    big_cate = scrapy.Field()
    small_cate = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    small_href = scrapy.Field()
    detail_href = scrapy.Field()
