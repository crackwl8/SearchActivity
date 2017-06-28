# -*- coding: utf-8 -*-

from scrapy import Item, Field


class ActivityItem(Item):
    title = Field()
    image_url = Field()
    link_url = Field()
    website = Field()
    valid = Field()
