# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CankaoItem(scrapy.Item):
    '''
    定义要保存的字段
    设置数据存储模板，用于结构化数据
    '''
    # define the fields for your item here like:
    url = scrapy.Field()
    img = scrapy.Field()
    content = scrapy.Field()
