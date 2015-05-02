# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class RentalAdItem(Item):
    """Rental Ad container (dictionary-like object) for scraped data"""
    title = Field()
    link = Field()
    description = Field()
    reference = Field()
    location = Field()
    price = Field()
    fees = Field()
    surface = Field()
    floor = Field()
    room = Field()
    constructedIn = Field()
