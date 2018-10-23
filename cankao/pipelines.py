# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem

class CankaoPipeline(object):
    '''
    保存到文件中
    '''
    def __init__(self):
        self.file = open('./download/papers.json', 'wb')

    # def open_spider(self, spider):
    #     '''
    #     spider是一个Spider对象，代表开启的Spider，当spider被开启时，调用这个方法
    #     数据库/文件的开启可以放在这里
    #     :param spider:
    #     :return:
    #     '''
    #     pass

    def process_item(self, item, spider):
        '''
        处理item，进行保存
        :param item:
        :param spider:
        :return:
        '''
        print(item['img'])
        if item['img']:
            line = json.dumps(dict(item)) + '\n'
            # 要转成字节类型，写入文件
            self.file.write(line.encode())
            # 给下一个pipline处理
            return item
        else:
            # 丢弃，后面的pipline也无法处理了
            raise DropItem('miss img in %s' % item)

    def close_spider(self, spider):
        '''
        spider被关闭的时候调用
        可以放置数据库/文件关闭的代码
        :param spider:
        :return:
        '''
        # pass
        self.file.close()
        print('pipine open file times %s' % 5)

    # @classmethod
    # def from_crawler(cls, crawler):
    #     '''
    #     类方法，用来创建pipeline实例，可以通过crawler来获取scarpy所有的核心组件，如配置
    #     :param crawler:
    #     :return:
    #     '''
    #     pass


from pymongo import MongoClient

class CankaoMongoPipeline(object):
    '''
    以mongo存储为例
    '''
    # 集合名
    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_port, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        '''
        类方法，用来创建pipeline实例，可以通过crawler来获取scarpy所有的核心组件，如配置
        :param crawler:
        :return:
        '''
        return cls(
            # 获取mongo连接
            mongo_uri = crawler.settings.get('MONGO_URI'),
            # 获取mongo连接
            mongo_port = crawler.settings.get('MONGO_PORT'),
            # 获取数据库，如果没有则用默认的item
            mongo_db = crawler.settings.get('MONGO_DATABASE', 'fecshop_test')
        )

    def open_spider(self, spider):
        '''
        spider是一个Spider对象，代表开启的Spider，当spider被开启时，调用这个方法
        数据库/文件的开启可以放在这里
        :param spider:
        :return:
        '''
        # 连接mongo
        self.client = MongoClient(self.mongo_uri, self.mongo_port)
        # 选择使用的数据库
        db_auth = self.client[self.mongo_db]
        # 验证登陆
        db_auth.authenticate("simpleUser", "simplePass")
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        '''
        处理item，进行保存
        :param item:
        :param spider:
        :return:
        '''
        # 向集合中添加数据
        self.db[self.collection_name].insert(dict(item))
        return item

    def close_spider(self, spider):
        '''
        spider被关闭的时候调用
        可以放置数据库/文件关闭的代码
        :param spider:
        :return:
        '''
        self.client.close()

import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
import os

class CankaoFilesPipeline(FilesPipeline):
    '''
    下载文件
    继承框架自带的FilesPipeline文件下载类
    '''

    def get_media_requests(self, item, info):
        '''
        重写此方法， 用来获取图片url进行下载
        :param item:
        :param info:
        :return:
        '''
        self.item = item
        yield scrapy.Request(item['img'])

    # def item_completed(self, results, item, info):
    #     '''
    #     下载完成后将会把结果送到这个方法
    #     :param results:
    #     :param item:
    #     :param info:
    #     :return:
    #     '''
    #     # print(results)
    #
    #     '''
    #     results 为下载返回的数据, 如下
    #     [(True, {'url': 'https://img3.doubanio.com/view/subject/m/public/s29816983.jpg', 'path': 'full/fced9acc2ecf23e0f96b9a2d9a442b02234f4388.jpg', 'checksum': 'ce0e7d543b37dbe3d21dd46ef8fcbd1b'})]
    #     图片下载成功时为True
    #     url 源图片地址
    #     path 下载的文件路径
    #     checksum md5 hash
    #     '''
    #     print(item)
    #     print(info)

    def file_path(self, request, response=None, info=None):
        '''
        重写要保存的文件路径，不使用框架自带的hash文件名
        :param request:
        :param response:
        :param info:
        :return:
        '''
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('FilesPipeline.file_key(url) method is deprecated, please use '
                          'file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # 后缀
        media_ext = os.path.splitext(url)[1]
        # 原名带后缀
        media_content = url.split("/")[-1]
        # 使用item中的内容
        # return 'full/%s%s' % (self.item['content'], media_ext)
        return 'full/%s' % (media_content)


import scrapy
from scrapy.pipelines.images import ImagesPipeline

class CankaoImagesPipeline(ImagesPipeline):
    '''
    继承框架自带的ImagesPipeline图片下载类，可以下载的同时生成不同尺寸的图片放在配置的目录下
    '''

    def get_media_requests(self, item, info):
        '''
        重写此方法， 用来获取图片url进行下载
        :param item:
        :param info:
        :return:
        '''
        yield scrapy.Request(item['img'])

    # def item_completed(self, results, item, info):
    #     '''
    #     下载完成后将会把结果送到这个方法
    #     :param results:
    #     :param item:
    #     :param info:
    #     :return:
    #     '''
    #     print(results)
    #
    #     '''
    #     results 为下载返回的数据, 如下
    #     [(True, {'url': 'https://img3.doubanio.com/view/subject/m/public/s29827942.jpg', 'path': 'full/ad6acfdbef4d9df208c0e010ed1efcc287cb6225.jpg', 'checksum': 'c5d853689829ba8731cbb27146d89573'})]
    #     图片下载成功时为True
    #     url 源图片地址
    #     path 下载的文件路径
    #     checksum md5 hash
    #     '''
    #     print(item)
    #     print(info)