# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
import random
import time

class Cankao2Spider(scrapy.Spider):
    '''
    测试随机User-agent头中间件和cookie管理
    '''
    name = 'cankao2'
    allowed_domains = ['wuxingxiangsheng.com']
    # start_urls = ['http://temp.wuxingxiangsheng.com/test/request']

    def start_requests(self):
        # cookiejar 参数用来自动管理cookie， 可以自动管理多个，根据cookiejar对应的值不同
        return [Request('http://temp.wuxingxiangsheng.com/test/request', meta = {'cookiejar':1})]

    def parse(self, response):
        '''
        解析
        :param response:
        :return:
        '''
        # 打印响应体
        print(response.body)
        # print(papers)
        salt = random.random()

        # 获取响应的cookie
        print(response.headers.getlist('Set-Cookie'))
        # 获取cookiejar对应的值 1
        print(response.meta['cookiejar'])
        time.sleep(120)
        # cookies 为自定义cookie值  meta = {'cookiejar' 为自动管理的cookie
        yield Request(url='http://temp.wuxingxiangsheng.com/test/request?salt=%s' % salt, cookies={'test':'test'},
                      meta = {'cookiejar':response.meta['cookiejar']}, callback=self.next)

    def next(self, response):
        # 获取请求携带的cookie， 自定义的加自动管理的
        cookie = response.request.headers.getlist('Cookie')
        print('请求时携带请求的Cookies：', cookie)
        print(response.body)