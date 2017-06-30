# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from items import ActivityItem


class SearchActivityMongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient("localhost", 27017)
        db = client.SearchActivity
        # del duplicate items
        # for url in db.activity.distinct("title"):  # 使用distinct方法，获取每一个独特的元素列表
        #     num = db.activity.count({"title": url})  # 统计每一个元素的数量
        #     for i in range(1, num):  # 根据每一个元素的数量进行删除操作，当前元素只有一个就不再删除
        #         print 'delete %s %d times ' % (url, i)
        #         # 注意后面的参数， 很奇怪，在mongo命令行下，它为1时，是删除一个元素，这里却是为0时删除一个
        #         db.activity.remove({"title": url}, 0)
        db.activity.create_index([("title", pymongo.ASCENDING)], background=True, unique=True)
        self.Res = db.activity

    def process_item(self, item, spider):
        print 'MongoDBItem', item
        """ 判断类型 存入MongoDB """
        if isinstance(item, ActivityItem):
            try:
                self.Res.insert(dict(item))
            except Exception:
                pass
        return item
