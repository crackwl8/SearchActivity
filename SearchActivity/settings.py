# -*- coding: utf-8 -*-

# Scrapy settings for searchActivity project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'SearchActivity'

SPIDER_MODULES = ['SearchActivity.spiders']
NEWSPIDER_MODULE = 'SearchActivity.spiders'

DOWNLOAD_DELAY = 1  # 间隔时间
LOG_LEVEL = 'INFO'  # 日志级别
CONCURRENT_REQUESTS = 100  # 默认为16
# CONCURRENT_ITEMS = 1
# CONCURRENT_REQUESTS_PER_IP = 1
REDIRECT_ENABLED = True
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'SearchActivity (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

RETRY_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
    "SearchActivity.middlewares.UserAgentMiddleware": 401,
    "SearchActivity.middlewares.CookiesMiddleware": 402,
    'SearchActivity.middlewares.JavaScriptMiddleware': 403,
}
ITEM_PIPELINES = {
    "SearchActivity.pipelines.SearchActivityMongoDBPipeline": 413,
}
