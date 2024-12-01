# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Recipe1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # description
    description = scrapy.Field()
    # image_url
    image_url = scrapy.Field()
    # ingredients
    ingredients = scrapy.Field()
    # steps
    steps = scrapy.Field()
    # title
    title = scrapy.Field()

    # pass
