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

DOWNLOAD_DELAY = 2  # 间隔时间
# LOG_LEVEL = 'INFO'  # 日志级别
CONCURRENT_REQUESTS = 50  # 默认为16
# CONCURRENT_ITEMS = 1
# CONCURRENT_REQUESTS_PER_IP = 1
REDIRECT_ENABLED = True
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'SearchActivity (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
    "SearchActivity.middlewares.UserAgentMiddleware": 401,
    "SearchActivity.middlewares.CookiesMiddleware": 402,
}
ITEM_PIPELINES = {
    "SearchActivity.pipelines.SearchActivityMongoDBPipeline": 403,
}
