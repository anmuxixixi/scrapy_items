import scrapy
from suningbook.items import SuningbookItem
from copy import deepcopy
import re
import json


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/']  # https://book.suning.com/

    def parse(self, response):
        item = SuningbookItem()
        # 大分类分组
        big_div_list = response.xpath('//div[@class="menu-list"]/div[@class="menu-item"]')
        for div in big_div_list:
            item['big_cate'] = div.xpath('.//h3/a/text()').extract_first()
            # 小分类分组
            small_a_list = div.xpath('.//dd/a')
            for a in small_a_list:
                item['small_cate'] = a.xpath('./text()').extract_first()
                item['small_href'] = a.xpath('./@href').extract_first()

                yield scrapy.Request(
                    item['small_href'],
                    callback=self.parse_small_cate,
                    meta={'item': deepcopy(item)},
                )

    def parse_small_cate(self, response):
        item = response.meta['item']
        li_list = response.xpath('//ul[@class="clearfix"]/li')
        if li_list is not None:
            for li in li_list:
                item['title'] = li.xpath('.//p[@class="sell-point"]/a/text()').extract_first()
                item['detail_href'] = 'https:' + li.xpath('.//p[@class="sell-point"]/a/@href').extract_first()

                yield scrapy.Request(
                    item['detail_href'],
                    callback=self.parse_detail,
                    meta={'item': deepcopy(item)}
                )

            # 翻页
            base_url = response.xpath('//div[@id="bottom_pager"]//a[1]/@href').extract_first()
            if base_url is not None:
                base_url1 = '-'.join(base_url.split('-')[0:2])
                base_url2 = '-'.join((base_url.split('-')[3:]))
                for i in range(1, 5):  # 翻五页
                    next_url = 'https://list.suning.com' + base_url1 + str(i) + base_url2
                    yield scrapy.Request(
                        next_url,
                        callback=self.parse_small_cate
                    )
        # 处理不同类型的界面，如散文诗
        else:
            li_list = response.xpath('//ul[@class="general clearfix"]/li')
            for li in li_list:
                item['title'] = li.xpath('.//div[@class="title-selling-point"]/a/text()').extract_first()
                item['detail_href'] = 'https:' + li.xpath(
                    './/div[@class="title-selling-point"]/a/@href').extract_first()

                yield scrapy.Request(
                    item['detail_href'],
                    callback=self.parse_detail,
                    meta={'item': deepcopy(item)}
                )

            # 翻页
            base_url3 = response.xpath('//div[@class="search-page page-fruits clearfix"]/a[1]/@href').extract_first()
            for i in range(1, 5):
                next_url = 'https://search.suning.com/' + base_url3[0:-1] + str(i)
                yield scrapy.Request(
                    next_url,
                    callback=self.parse_small_cate
                )

    def parse_detail(self, response):
        item = response.meta['item']
        if '很抱歉,此商品不存在' not in response.text:
            item['author'] = response.xpath('//ul[@class="bk-publish clearfix"]/li[1]/text()').extract_first()

            url_text = response.text
            part_num = re.findall(r'\"partNumber\":\"(.*?)\"', url_text)[0]
            vendorCode = re.findall(r'\"vendorCode\":\"(.*?)\"', url_text)[0]
            price_url = 'https://pas.suning.com/nspcsale_0_' + part_num +'_'+ part_num +'_'+ vendorCode + '_100_025_0250199_502282_1000173_9173_11365_Z001___R9011196_0.6____0001400NH____0___0.0_2__502320_502678_.html?callback=pcData'

            yield scrapy.Request(
                price_url,
                callback=self.parsr_price,
                meta={'item': deepcopy(item)},
            )

    def parsr_price(self, response):
        item = response.meta['item']
        price_text = response.text
        pcData = re.findall(r'pcData\((.*)\)', price_text, re.S)[0]
        price_json = json.loads(pcData)
        item['price'] = price_json['data']['price']['saleInfo'][0]['netPrice']

        yield item
