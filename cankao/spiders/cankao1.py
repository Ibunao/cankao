# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from ..items import CankaoItem

class Cankao1Spider(scrapy.Spider):
    '''
    爬取豆瓣图书图片，单层爬虫
    '''
    # 爬虫名，必填
    name = 'cankao1'
    # 允许访问的域名，只允许访问这个域名下的url
    allowed_domains = ['douban.com']
    # 开始的url
    start_urls = ['https://book.douban.com/']
    # 自定义配置，会覆盖项目配置
    custom_settings = {}

    # def start_requests(self):
    #     '''
    #     重写父类的方法，父类的方法默认从start_urls中读取开始爬取
    #     一般不需要重写，但是如果第一步就是登陆的话就需要重写了
    #     :return:
    #     '''

    def parse(self, response):
        '''
        解析
        :param response:
        :return:
        '''
        # 打印响应体
        # print(response.body)
        papers = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div[2]/div/div/ul[2]/li')
        # print(papers)
        for paper in papers:
            url = paper.xpath('.//div/a/@href').extract_first()
            img = paper.xpath('.//div/a/img/@src').extract_first()
            content = paper.xpath('.//div/div/a/text()').extract_first()
            print(url, img, content)
            item = CankaoItem(url = url, img = img, content = content)
            yield item

        # time.sleep(5000)
        # 分析下一个请求,进行请求（测试一下allowed_domains，不属于不能请求）
        # yield Request(url='http://www.bunao.win')
