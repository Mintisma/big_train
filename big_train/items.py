# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import datetime

import scrapy
from scrapy import Field
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader


def create_date(value):
    try:
        create_date = datetime.datetime.strptime(value, '%Y%m%d').date()
    except Exception as e:
        create_date = datetime.datetime.strptime('00010101', '%Y%m%d').date()
    return create_date


def join_text(value):
    value = '\n'.join(value)
    return value


class SinaLoader(ItemLoader):
    default_output_processor = TakeFirst()


class SinaItem(scrapy.Item):
    table = 'sina_new'
    company = Field()
    title = Field()
    content = Field(
        input_processor=join_text,
    )
    date = Field(
        input_processor = MapCompose(create_date, )
    )
    type = Field()
    url = Field()