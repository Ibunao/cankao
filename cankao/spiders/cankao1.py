# -*- coding: utf-8 -*-
import scrapy


class Cankao1Spider(scrapy.Spider):
    # 爬虫名，必填
    name = 'cankao1'
    # 允许访问的域名
    allowed_domains = ['douban.com']
    # 开始的url
    start_urls = ['http://douban.com/']

    def parse(self, response):
        '''
        解析
        :param response:
        :return:
        '''
        pass
