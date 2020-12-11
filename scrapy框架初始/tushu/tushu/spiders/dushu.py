import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DushuSpider(CrawlSpider):
    name = 'dushu'
    allowed_domains = ['dushu.com']
    start_urls = ['http://dushu.com/book/']

    rules = (
        # 提取每一个大类的href
        # Rule(LinkExtractor(r'/book/\d+\.html'),follow=True),
        Rule(LinkExtractor(restrict_css=r'.sub-catalog'),follow=True),

        # 进入到每一个大类后提取分页的href
        Rule(LinkExtractor(r'/book/\d+?_\d+?\.html'),
             follow=True),

        # 详情页提取数据
        Rule(LinkExtractor(r'/book/\d+/'),
             callback='parse_item',
             follow=False)
    )

    def parse_item(self, response):
        item ={}
        item['title'] = response.xpath('//div[@class="book-title"]/h1/text()').extract_first()
        item['price'] = response.xpath('//p[@class="price"]/span/text()').extract_first()
        item['author'] = response.xpath('//div[@class="book-details-left"]/table//tr[1]/td[2]/text()').extract_first()

        print(item)
