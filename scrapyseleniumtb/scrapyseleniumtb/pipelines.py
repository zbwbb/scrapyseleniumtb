# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class ScrapyseleniumtbPipeline(object):

    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    # spider 启动的时候，执行该方法，主要进行一些初始化的工作
    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        # 插入 json 数据
        self.db[item.collection].insert(dict(item))

    # 断开连接
    def close_spider(self, spider):
        self.client.close()
