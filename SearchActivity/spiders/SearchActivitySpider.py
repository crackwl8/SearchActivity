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

from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
display.start()
web_driver = webdriver.Chrome("/usr/local/bin/chromedriver")  # Firefox()

class Spider(CrawlSpider):
    name = 'searchActivitySpider'
    allowed_domains = ['amazon.com', 'ebay.com', 'wish.com']
    start_urls = []
    logging.getLogger("requests").setLevel(logging.WARNING
                                          )  # 将requests的日志级别设成WARNING
    logging.basicConfig(
        level=logging.INFO,
        format=
        '%(asctime)s %(filename)s[line:%(lineno)d] %(process)d %(thread)d %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='cataline.log',
        filemode='w')

    def __init__(self):  # 初始化类
        self.waiting_list = []
        self.finish_list = []
        self.driver = web_driver
        self.driver.set_page_load_timeout(20)
        self.driver.set_script_timeout(5)

    def __del__(self):
        if self.driver is not None:
            self.driver.quit()

    # test = True
    def start_requests(self):
        hosts = [
                 # {'url': 'https://www.tmall.com', 'call_back': self.parse_tmall_key},
                 # {'url': 'https://item.jd.com', 'call_back': self.parse_jd_key},
                 # {'url': 'https://www.amazon.cn', 'call_back': self.parse_amazon_key},
                 {'url': 'https://www.amazon.com', 'call_back': self.parse_amazon_foreign_key},
                 {'url': 'https://www.ebay.com', 'call_back': self.parse_ebay_foreign_key},
                 # {'url': 'https://www.wish.com', 'call_back': self.parse_wish_foreign_key},
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
            # logging.error(self.waiting_list)
            pass
        self.finish_list.append(response.url)
        logging.info(
            ' request url callback:----->' + response.url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))

        # logging.info(selector)
        # divs = selector.xpath('//div[@class="tm-fcs-panel"]/dl[@class="tm-promo-panel"]/dd/div[@class="tm-promo-price"]')
        viewkey = None
        price = 0
        if 'detail.tmall.com' in response.url:
            prices = selector.css('.tm-price::text').extract()
            if prices and len(prices) > 0:
                price = prices[0]
            divs = selector.css('.tm-promo-type')
            for div in divs:
                for desc in TMALL_DESC:
                    viewkey = re.findall('.*?' + desc + '.*?', div.extract())
                    if viewkey:
                        break
        if viewkey:
            yield self.parse_tmall_info(response, price)
        url_next = selector.xpath(
            '//a/@href').extract()
        logging.info(len(url_next))
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
            if (url not in self.finish_list) and (url not in self.waiting_list) and ('tmall.com' in url) and ('search_product' not in url) \
                    and ('www.tmall.com' not in url) and valid_url:
                if len(self.waiting_list) < 1000000:
                    self.waiting_list.append(url)
                else:
                    logging.error('too many waiting url!!!!!')
                # logging.debug(' next page:----->' + url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))
                yield Request(url=url,
                              callback=self.parse_tmall_key, errback=self.parse_err)

    def parse_tmall_info(self, response, price):
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
        actItem['price'] = float(price)
        logging.debug(' title:%s link_url:%s price:%s' % (title, link_url, price))
        return actItem

    def parse_jd_key(self, response):
        selector = Selector(response)
        try:
            self.waiting_list.remove(response.url)
        except ValueError:
            # logging.debug(self.waiting_list)
            pass
        self.finish_list.append(response.url)
        logging.info(
            ' request url callback:----->' + response.url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))

        # logging.info(selector)
        # divs = selector.xpath('//div[@class="tm-fcs-panel"]/dl[@class="tm-promo-panel"]/dd/div[@class="tm-promo-price"]')
        viewkey = None
        price = 0
        if 'item.jd.com' in response.url:
            prices = selector.css('.price::text').extract()
            if prices and len(prices) > 0:
                price = prices[0]
            divs = selector.css('.summary-promotion')
            for div in divs:
                for desc in JD_DESC:
                    viewkey = re.findall('.*?' + desc + '.*?', div.extract())
                    if viewkey:
                        break
        if viewkey:
            yield self.parse_jd_info(response, price)
        url_next = selector.xpath(
            '//*/@href').extract()
        logging.debug(len(url_next))
        for url in url_next:
            if url.startswith('//'):
                url = 'https:' + url
            elif (not url.startswith('http')):
                url = 'https://' + url
            valid_url = True
            for domain in JD_EXCEPT_DOMAIN:
                if domain in url:
                    valid_url = False
                    break
            if (url not in self.finish_list) and (url not in self.waiting_list) and ('jd.com' in url) \
                    and ('www.jd.com' not in url) and valid_url:
                if len(self.waiting_list) < 1000000:
                    self.waiting_list.append(url)
                else:
                    logging.error('too many waiting url!!!!!')
                # logging.debug(' next page:----->' + url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))
                yield Request(url=url,
                              callback=self.parse_jd_key, errback=self.parse_err)

    def parse_jd_info(self, response, price):
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
        actItem['price'] = float(price)
        logging.debug(' title:%s link_url:%s price:%s' % (title, link_url, price))
        return actItem

    def parse_amazon_key(self, response):
        selector = Selector(response)
        try:
            self.waiting_list.remove(response.url)
        except ValueError:
            # logging.debug(self.waiting_list)
            pass
        self.finish_list.append(response.url)
        logging.info(
            ' request url callback:----->' + response.url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))

        # logging.info(selector)
        # divs = selector.xpath('//div[@class="tm-fcs-panel"]/dl[@class="tm-promo-panel"]/dd/div[@class="tm-promo-price"]')
        viewkey = None
        price = 0
        if 'www.amazon.cn/gp/product' in response.url:
            prices = selector.css('#priceblock_dealprice::text').extract()
            if prices and len(prices) > 0:
                price = prices[0][1:]
            divs = selector.css('.a-size-base.a-color-secondary.apl_label')
            for div in divs:
                for desc in AMAZON_DESC:
                    viewkey = re.findall('.*?' + desc + '.*?', div.extract())
                    if viewkey:
                        break
        if viewkey:
            yield self.parse_amazon_info(response, price)
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
            if (url not in self.finish_list) and (url not in self.waiting_list) and ('www.amazon.cn' in url) and valid_url:
                if len(self.waiting_list) < 1000000:
                    self.waiting_list.append(url)
                else:
                    logging.error('too many waiting url!!!!!')
                # logging.debug(' next page:----->' + url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))
                yield Request(url=url,
                              callback=self.parse_amazon_key, errback=self.parse_err)

    def parse_amazon_info(self, response, price):
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
        import string
        actItem['price'] = string.atof(price.split()[0])
        logging.debug(' title:%s link_url:%s price:%s' % (title, link_url, price))
        return actItem

    def parse_amazon_foreign_key(self, response):
        selector = Selector(response)
        try:
            self.waiting_list.remove(response.url)
        except ValueError:
            # logging.debug(self.waiting_list)
            pass
        self.finish_list.append(response.url)
        logging.info(
            ' request url callback:----->' + response.url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))

        # logging.info(selector)
        # divs = selector.xpath('//div[@class="tm-fcs-panel"]/dl[@class="tm-promo-panel"]/dd/div[@class="tm-promo-price"]')
        viewkey = None
        price = 0
        # 商品详情的页面才处理，要取出价格、卖家、品牌、评论、库存等信息
        if 'www.amazon.com/dp/' in response.url or 'www.amazon.com/gp/' in response.url:
            prices = selector.css('.a-span12.a-color-price.a-size-base::text').extract()
            if prices and len(prices) > 0:
                price = prices[0][1:]
            divs = selector.css('.a-color-secondary.a-size-base.a-text-right.a-nowrap')
            for div in divs:
                for desc in AMAZON_DESC:
                    viewkey = re.findall('.*?' + desc + '.*?', div.extract())
                    if viewkey:
                        break
        if viewkey:
            yield self.parse_amazon_info(response, price)

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
            if (url not in self.finish_list) and (url not in self.waiting_list) and ('www.amazon.cn' in url) and valid_url:
                if len(self.waiting_list) < 1000000:
                    self.waiting_list.append(url)
                else:
                    logging.error('too many waiting url!!!!!')
                # logging.debug(' next page:----->' + url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))
                yield Request(url=url,
                              callback=self.parse_amazon_key, errback=self.parse_err)

    def parse_ebay_foreign_key(self, response):
        selector = Selector(response)
        try:
            self.waiting_list.remove(response.url)
        except ValueError:
            # logging.debug(self.waiting_list)
            pass
        self.finish_list.append(response.url)
        logging.info(
            ' request url callback:----->' + response.url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))

        # logging.info(selector)
        # divs = selector.xpath('//div[@class="tm-fcs-panel"]/dl[@class="tm-promo-panel"]/dd/div[@class="tm-promo-price"]')
        viewkey = None
        price = 0
        if 'www.ebay.com/' in response.url:
            prices = selector.css('.price-bin::text').extract()
            if prices and len(prices) > 0:
                price = prices[0][1:]
                print price
            divs = selector.css('.a-color-secondary.a-size-base.a-text-right.a-nowrap')
            for div in divs:
                for desc in AMAZON_DESC:
                    viewkey = re.findall('.*?' + desc + '.*?', div.extract())
                    if viewkey:
                        break
        if viewkey:
            yield self.parse_amazon_info(response, price)
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
            if (url not in self.finish_list) and (url not in self.waiting_list) and ('www.amazon.cn' in url) and valid_url:
                if len(self.waiting_list) < 1000000:
                    self.waiting_list.append(url)
                else:
                    logging.error('too many waiting url!!!!!')
                # logging.debug(' next page:----->' + url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))
                yield Request(url=url,
                              callback=self.parse_amazon_key, errback=self.parse_err)

    def parse_wish_foreign_key(self, response):
        selector = Selector(response)
        try:
            self.waiting_list.remove(response.url)
        except ValueError:
            # logging.debug(self.waiting_list)
            pass
        self.finish_list.append(response.url)
        logging.info(
            ' request url callback:----->' + response.url + ' waiting %s finished %s' % (len(self.waiting_list), len(self.finish_list)))

        # logging.info(selector)
        # divs = selector.xpath('//div[@class="tm-fcs-panel"]/dl[@class="tm-promo-panel"]/dd/div[@class="tm-promo-price"]')
        viewkey = None
        price = 0
        if 'www.wish.com/' in response.url:
            prices = selector.css('.actual-price').extract()
            print 'prices', prices
            if prices and len(prices) > 0:
                price = prices[0][1:]
                print prices
            divs = selector.css('.a-color-secondary.a-size-base.a-text-right.a-nowrap')
            for div in divs:
                for desc in AMAZON_DESC:
                    viewkey = re.findall('.*?' + desc + '.*?', div.extract())
                    if viewkey:
                        break
        if viewkey:
            yield self.parse_amazon_info(response, price)


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
