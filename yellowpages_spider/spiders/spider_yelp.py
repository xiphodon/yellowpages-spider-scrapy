#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/26 10:38
# @Author  : GuoChang
# @Site    : https://github.com/xiphodon
# @File    : spider_yelp.py
# @Software: PyCharm

import scrapy


class YelpSpider(scrapy.Spider):
    """
    德国黄页爬虫
    """
    name = 'yelp_spider'

    def start_requests(self):
        """
        起始请求
        :return:
        """
        urls = ['https://www.yelp.com/search'
                '?find_desc=Mobile+Phone+Accessories'
                '&find_loc=Tokyo,+%E6%9D%B1%E4%BA%AC%E9%83%BD,+JP']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list_page)

    def parse_list_page(self, response):
        """
        解析列表响应
        :param response:
        :return:
        """
        item_href_list = response.xpath('//ul/li//div[@class="media-story"]/h3/span/a/@href')
        for item_href in item_href_list:
            item_href_str = item_href.extract()
            yield response.follow(item_href_str, callback=self.parse_detail_page)
        # 下一页
        next_page_href = response.xpath('//div[@class="arrange_unit"]/a/@href')[-1].extract()
        if next_page_href:
            # yield response.follow(next_page_href, callback=self.parse_list_page)
            pass

    def parse_detail_page(self, response):
        """
        解析详情页
        :param response:
        :return:
        """
        company_name = response.xpath('//h1[contains(@class,"biz-page-title")]/text()').extract_first()
        company_name = str(company_name).strip()
        print(company_name)

        company_address_list = response.xpath('//strong[@class="street-address"]/address/text()')
        company_address = ','.join([str(item.extract()).strip() for item in company_address_list])
        print(company_address)

        company_tel = response.xpath('//span[@class="biz-phone"]/text()').extract_first()
        company_tel = str(company_tel).strip()
        print(company_tel)

        company_website = response.xpath('//span[contains(@class,"biz-website")]/a/text()').extract_first()
        company_website = str(company_website).strip()
        print(company_website)
        return None
