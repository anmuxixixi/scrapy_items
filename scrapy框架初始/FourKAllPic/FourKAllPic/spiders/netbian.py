import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class NetbianSpider(CrawlSpider):
    name = 'netbian'
    allowed_domains = ['pic.netbian.com']
    start_urls = ['http://pic.netbian.com/']

    rules = (
        # 提取每一个大类的href 4K风景 4K美女 4K游戏
        Rule(LinkExtractor(restrict_xpaths='//div[@class="classify clearfix"]'),follow=True),

        # 翻页，提取所有翻页的href
        Rule(LinkExtractor(allow=r'/4kfengjing/index_\d+\.html'),follow=True),

        # 提取照片详情页的href 一定要记住LinkExtractor提取的是a标签的href
        Rule(LinkExtractor(allow=r'/tupian/\d+\.html'), callback='parse_item',follow=False),
    )


    def parse_item(self, response):
        item = {}
        item['cate_name'] = response.xpath('//div[@class="infor"]/p[1]//a/text()').extract_first()
        item['title'] = response.xpath('//div[@class="photo-hd"]/h1/text()').extract_first()
        item['image_urls'] ='http://pic.netbian.com'+ response.xpath('//div[@class="photo-pic"]/a/img/@src').extract_first()

        print(item)

        yield item