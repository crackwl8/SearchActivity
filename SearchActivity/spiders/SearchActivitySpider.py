#coding:utf-8
import requests
import logging
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from SearchActivity.items import ActivityItem
from SearchActivity.search_type import PH_TYPES, TMALL_DESC, TMALL_EXCEPT_DOMAIN, JD_DESC, JD_EXCEPT_DOMAIN, AMAZON_DESC, AMAZON_EXCEPT_DOMAIN
from scrapy.http import Request
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import re
import json
import random
from selenium import webdriver

web_driver = webdriver.Chrome("/Users/wulei/Downloads/chromedriver")

class Spider(CrawlSpider):
    name = 'searchActivitySpider'
    allowed_domains = ['tmall.com', 'taobao.com', 'jd.com', 'amazon.cn']
    start_urls = []
    logging.getLogger("requests").setLevel(logging.WARNING
                                          )  # 将requests的日志级别设成WARNING
    logging.basicConfig(
        level=logging.DEBUG,
        format=
        '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='cataline.log',
        filemode='w')

    def __init__(self):  # 初始化类
        self.waiting_list = []
        self.finish_list = []
        self.driver = web_driver

    def __del__(self):
        if self.driver is not None:
            self.driver.quit()

    # test = True
    def start_requests(self):
        hosts = [
                 {'url': 'https://www.tmall.com', 'call_back': self.parse_tmall_key},
                 {'url': 'https://www.jd.com', 'call_back': self.parse_jd_key},
                 {'url': 'https://www.amazon.cn', 'call_back': self.parse_amazon_key},
                ]
        for host in hosts:
            self.waiting_list.append(host['url'])
            yield Request(url='%s' % (host['url']),
                          callback=host['call_back'], errback=self.parse_err)

    def parse_tmall_key(self, response):
        selector = Selector(response)
        try:
            self.waiting_list.remove(response.url)
        except ValueError:
            # logging.debug(self.waiting_list)
            pass
        self.finish_list.append(response.url)
        logging.debug(
            ' request url callback:----->' + response.url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))
        self.driver.get(response.url)
        selector = Selector(text=self.driver.page_source)
        # logging.info(selector)
        # divs = selector.xpath('//div[@class="tm-fcs-panel"]/dl[@class="tm-promo-panel"]/dd/div[@class="tm-promo-price"]')
        viewkey = None
        if 'detail.tmall.com' in response.url:
            divs = selector.css('.tm-promo-type')
            for div in divs:
                for desc in TMALL_DESC:
                    viewkey = re.findall('.*?' + desc + '.*?', div.extract())
                    if viewkey:
                        break
        if viewkey:
            yield self.parse_tmall_info(response)
        url_next = selector.xpath(
            '//a/@href').extract()
        # logging.debug(len(url_next))
        for url in url_next:
            if url.startswith('//'):
                url = 'https:' + url
            elif not url.startswith('http'):
                url = 'https://' + url
            valid_url = True
            for domain in TMALL_EXCEPT_DOMAIN:
                if domain in url:
                    valid_url = False
                    break
            if (url not in self.finish_list) and ('tmall.com' in url) and ('search_product' not in url) \
                    and ('www.tmall.com' not in url) and valid_url:
                self.waiting_list.append(url)
                # logging.debug(' next page:----->' + url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))
                yield Request(url=url,
                              callback=self.parse_tmall_key, errback=self.parse_err)

    def parse_tmall_info(self, response):
        actItem = ActivityItem()
        selector = Selector(response)
        _ph_info = selector.xpath('//title/text()').extract()
        title = _ph_info[0]
        actItem['title'] = title
        image_url = ''
        actItem['image_url'] = image_url
        link_url = response.url
        actItem['link_url'] = link_url
        actItem['website'] = 'tmall'
        actItem['valid'] = True
        logging.debug(' title:%s link_url:%s' % (title, link_url))
        return actItem

    def parse_jd_key(self, response):
        selector = Selector(response)
        try:
            self.waiting_list.remove(response.url)
        except ValueError:
            # logging.debug(self.waiting_list)
            pass
        self.finish_list.append(response.url)
        logging.debug(
            ' request url callback:----->' + response.url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))
        self.driver.get(response.url)
        selector = Selector(text=self.driver.page_source)
        # logging.info(selector)
        # divs = selector.xpath('//div[@class="tm-fcs-panel"]/dl[@class="tm-promo-panel"]/dd/div[@class="tm-promo-price"]')
        viewkey = None
        if 'item.jd.com' in response.url:
            divs = selector.css('.summary-promotion')
            for div in divs:
                for desc in JD_DESC:
                    viewkey = re.findall('.*?' + desc + '.*?', div.extract())
                    if viewkey:
                        break
        if viewkey:
            yield self.parse_jd_info(response)
        url_next = selector.xpath(
            '//*/@href').extract()
        logging.debug(len(url_next))
        for url in url_next:
            if url.startswith('//'):
                url = 'https:' + url
            elif (not url.startswith('http')) and url.startswith('/'):
                url = 'https://' + url
            valid_url = True
            for domain in JD_EXCEPT_DOMAIN:
                if domain in url:
                    valid_url = False
                    break
            if (url not in self.finish_list) and ('jd.com' in url) and ('search_product' not in url) \
                    and ('www.jd.com' not in url) and valid_url:
                self.waiting_list.append(url)
                # logging.debug(' next page:----->' + url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))
                yield Request(url=url,
                              callback=self.parse_jd_key, errback=self.parse_err)

    def parse_jd_info(self, response):
        actItem = ActivityItem()
        selector = Selector(response)
        _ph_info = selector.xpath('//title/text()').extract()
        title = _ph_info[0]
        actItem['title'] = title
        image_url = ''
        actItem['image_url'] = image_url
        link_url = response.url
        actItem['link_url'] = link_url
        actItem['website'] = 'jd'
        actItem['valid'] = True
        logging.debug(' title:%s link_url:%s' % (title, link_url))
        return actItem

    def parse_amazon_key(self, response):
        selector = Selector(response)
        try:
            self.waiting_list.remove(response.url)
        except ValueError:
            # logging.debug(self.waiting_list)
            pass
        self.finish_list.append(response.url)
        logging.debug(
            ' request url callback:----->' + response.url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))
        self.driver.get(response.url)
        selector = Selector(text=self.driver.page_source)
        # logging.info(selector)
        # divs = selector.xpath('//div[@class="tm-fcs-panel"]/dl[@class="tm-promo-panel"]/dd/div[@class="tm-promo-price"]')
        viewkey = None
        if 'www.amazon.cn/gp/product' in response.url:
            divs = selector.css('.a-size-base.a-color-secondary.apl_label')
            for div in divs:
                for desc in AMAZON_DESC:
                    viewkey = re.findall('.*?' + desc + '.*?', div.extract())
                    if viewkey:
                        break
        if viewkey:
            yield self.parse_amazon_info(response)
        url_next = selector.xpath(
            '//*/@href').extract()
        logging.debug(len(url_next))
        for url in url_next:
            if url.startswith('//'):
                url = 'https:' + url
            elif (not url.startswith('http')) and url.startswith('/'):
                url = 'https://www.amazon.cn' + url
            valid_url = True
            for domain in AMAZON_EXCEPT_DOMAIN:
                if domain in url:
                    valid_url = False
                    break
            if (url not in self.finish_list) and ('www.amazon.cn' in url) and valid_url:
                self.waiting_list.append(url)
                # logging.debug(' next page:----->' + url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))
                yield Request(url=url,
                              callback=self.parse_amazon_key, errback=self.parse_err)

    def parse_amazon_info(self, response):
        actItem = ActivityItem()
        selector = Selector(response)
        _ph_info = selector.xpath('//title/text()').extract()
        title = _ph_info[0]
        actItem['title'] = title
        image_url = ''
        actItem['image_url'] = image_url
        link_url = response.url
        actItem['link_url'] = link_url
        actItem['website'] = 'amazon'
        actItem['valid'] = True
        logging.debug(' title:%s link_url:%s' % (title, link_url))
        return actItem

    def parse_err(self, failure):
        # log all failures
        # logging.error(repr(failure))
        url = ''
        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            url = response.url
            # selector = Selector(response)
            # logging.info(selector)
            logging.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            url = request.url
            logging.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            url = request.url
            logging.error('TimeoutError on %s', request.url)

        if url:
            try:
                self.waiting_list.remove(url)
            except ValueError:
                # logging.debug(self.waiting_list)
                pass
            self.finish_list.append(url)
        logging.debug('request url err callback:------>' + url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))