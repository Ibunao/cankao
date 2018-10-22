# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem

class CankaoPipeline(object):
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


import pymongo

class CankaoMongoPipeline(object):
    '''
    以mongo存储为例
    '''
    # 集合名
    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
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
        self.client = pymongo.MongoClient(self.mongo_uri)
        db_auth = self.client.admin
        db_auth.authenticate("simpleUser", "simplePass")
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        '''
        处理item，进行保存
        :param item:
        :param spider:
        :return:
        '''
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
