# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

class FourkallpicPipeline:
    def process_item(self, item, spider):
        return item


class MyFourKPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        url = item['image_urls']
        yield Request(url,meta={'item':item})

    # def item_completed(self, results, item, info):
    #     image_paths = [x for ok, x in results if ok]
    #     item['image_path'] = image_paths  # 注意这里的item['image_path']需要在items文件里面事先定义好,可以按照自己的喜好取名
    #     return item


    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        file_name = item['cate_name']+'/'+item['title']+'.jpg'
        return file_name
