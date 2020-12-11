# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

class SuningbookPipeline:
    def open_spider(self,spider):
        client = MongoClient()
        self.collection = client['苏宁图书']['books']

    def process_item(self, item, spider):
        # self.collection.insert(dict(item))
        item['author'] = self.parse_author(item['author'])
        item['title'] = self.parse_title(item['title'])
        new_item = {'标题':item['title'],'作者':item['author'],'类别':item['small_cate'],
                    '价格':item['price']}
        self.collection.insert(new_item)
        print(item['title'],'   爬取结束   ...')

        return item

    def parse_author(self,content):
        content = content.strip()
        return content

    def parse_title(self,content):
        content = re.sub('\n','',content)
        return content