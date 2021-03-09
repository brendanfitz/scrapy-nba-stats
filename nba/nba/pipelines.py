# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from os import environ


class MongoDBPipeline:

    CONFIG = {
        'host': environ['SCRAPY_MONGODB_SERVER'],
        'port': int(environ['SCRAPY_MONGODB_PORT']),
        'db': environ['SCRAPY_MONGODB_DATABASE'],
    }

    def open_spider(self, spider):
        self.client = MongoClient(
            host=self.CONFIG['host'],
            port=self.CONFIG['port']
        )
        self.db = self.client[self.CONFIG['db']]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = ItemAdapter(item).asdict()
        update = {"$set": data}
        # perform upsert
        self.db[spider.name].update_one(filter=data, update=update, upsert=True)

        return item
    
