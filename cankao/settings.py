# -*- coding: utf-8 -*-

# Scrapy settings for cankao project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'cankao'

SPIDER_MODULES = ['cankao.spiders']
NEWSPIDER_MODULE = 'cankao.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#  客户端 user-agent请求头
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'

#  客户端 user-agent请求头 随机使用一个
USER_AGENTS = [
   'Mozilla/5.1 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
   'Mozilla/5.2 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
   'Mozilla/5.3 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
   ]

# Obey robots.txt rules
# 是否遵守robot协议
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 并发请求数
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'cankao.middlewares.CankaoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# 下载中间件
DOWNLOADER_MIDDLEWARES = {
   'cankao.middlewares.RandomUserAgent': 100,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 激活pipline，从低到高开始执行
ITEM_PIPELINES = {
   # 'cankao.pipelines.CankaoPipeline': 300,
   # 'cankao.pipelines.CankaoMongoPipeline': 500,
   # 'cankao.pipelines.CankaoFilesPipeline': 600,
   # 'cankao.pipelines.CankaoImagesPipeline': 700,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# mongo的配置信息
MONGO_URI = '118.25.38.240'
MONGO_PORT = 27017
MONGO_DATABASE = 'fecshop_test'

'''
FilesPipeline 配置
'''
# 设置文件存放位置
FILES_STORE = './download/files'
# 设置文件过期时间30天
FILES_EXPIRES = 30

'''
ImagesPipeline 配置
'''
# 设置图片路径
IMAGES_STORE = './download/images'
# 制作缩略图
IMAGES_THUMBS = {
   'small': (50, 50),
   'big': (270, 270)
}
# 设置图片过期时间30天
IMAGES_EXPIRES = 30
# 过滤下载图片的大小
# 过滤条件：最小图片尺寸
# IMAGES_MIN_HEIGH = 10
# IMAGES_MIN_WIDTH = 10
