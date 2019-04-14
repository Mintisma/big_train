# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.http import Request

from big_train.items import SinaLoader, SinaItem
from big_train.utils.company_site2name import site2name
from big_train.utils.response_url2date import url2date


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sz002668',
                  'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sh600690',
                  'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sz002242',
                  'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sh603726',
                  'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sz002032',
                  'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sz002759',
                  'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sh603996',
                  'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sz000651',
                  'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sz002508',
                  'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sz000100',
                  'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sz000333',
                  'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sh600839',
                  'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sz000921'
                  ]

    def parse(self, response):
        urls = response.xpath('//ul/a/@href').extract()
        titles = response.xpath('//ul/a/text()').extract()
        company_name = site2name(response.url)

        for url in urls:
            index_num = urls.index(url)
            text = titles[index_num]
            if '公告' in text:
                yield Request(url, callback=self.parse_post, meta={'company_name': company_name})
            else:
                yield Request(url, callback=self.parse_news, meta={'company_name': company_name})
        next_page = response.xpath('//a[text()="下一页"]/@href').extract_first('')
        if next_page:
            yield Request(next_page, callback=self.parse)

    def parse_news(self, response):
        item_loader = SinaLoader(SinaItem(), response=response)

        date = url2date(response.url)
        company_name = response.meta.get('company_name', '')
        item_loader.add_value('company', company_name)
        item_loader.add_value('type', 'news')
        item_loader.add_value('date', date)
        item_loader.add_xpath('title', '//h1/text()')
        item_loader.add_xpath('content', '//div[@id="artibody"]/p/text()')
        item_loader.add_value('url', response.url)

        sina_item = item_loader.load_item()
        yield sina_item

    def parse_post(self, response):
        item_loader = SinaLoader(SinaItem(), response=response)

        date = url2date(response.url)
        company_name = response.meta.get('company_name', '')
        item_loader.add_value('company', company_name)
        item_loader.add_value('type', 'post')
        item_loader.add_value('date', date)
        item_loader.add_xpath('title', '//h1/text()')
        item_loader.add_xpath('content', '//div[@id="artibody"]/div/p/text()')
        item_loader.add_value('url', response.url)

        sina_item = item_loader.load_item()
        yield sina_item
