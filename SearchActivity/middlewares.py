# encoding=utf-8
import random
from user_agents import agents
import json
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import logging

class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class CookiesMiddleware(object):
    """ 换Cookie """
    cookie = {
        'platform': 'pc',
        'ss': '367701188698225489',
        'bs': '%s',
        'RNLBSERVERID': 'ded6699',
        'FastPopSessionRequestNumber': '1',
        'FPSRN': '1',
        'performance_timing': 'home',
        'RNKEY': '40859743*68067497:1190152786:3363277230:1'
    }

    def process_request(self, request, spider):
        bs = ''
        for i in range(32):
            bs += chr(random.randint(97, 122))
        _cookie = json.dumps(self.cookie) % bs
        request.cookies = json.loads(_cookie)

class JavaScriptMiddleware(object):
    def process_request(self, request, spider):
        # logging.info("JS is starting...")

        try:
            spider.driver.get(request.url)
            # time.sleep(1)
            # js = "var q=document.documentElement.scrollTop=10000"
            # driver.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
            # time.sleep(1)
        except Exception as exc:
            logging.error('err url:' + request.url)
            logging.error(exc)
            spider.driver.quit()
            spider.driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
            spider.driver.set_page_load_timeout(20)
            spider.driver.set_script_timeout(5)
            pass

        body = spider.driver.page_source
        # logging.info("访问" + request.url)
        return HtmlResponse(spider.driver.current_url, body=body, encoding='utf-8', request=request)
