#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/26 10:38
# @Author  : GuoChang
# @Site    : https://github.com/xiphodon
# @File    : spider_germany.py
# @Software: PyCharm

import scrapy


class GermanySpider(scrapy.Spider):
    """
    德国黄页爬虫
    """
    name = 'germany_spider'

    def start_requests(self):
        """
        起始请求
        :return:
        """
        urls = ['https://www.gelbeseiten.de/haushaltswaren']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list_page)

    def parse_list_page(self, response):
        """
        解析列表响应
        :param response:
        :return:
        """
        item_href_list = response.xpath('//div[@id="gs_treffer"]/article/@data-href')
        for item_href in item_href_list:
            item_href_str = item_href.extract()
            yield scrapy.Request(item_href_str, callback=self.parse_detail_page)
        # 下一页
        next_page_href = response.xpath('//a[@title="Weiter"]/@href').extract_first()
        if next_page_href:
            yield scrapy.Request(next_page_href, callback=self.parse_list_page)

    def parse_detail_page(self, response):
        """
        解析详情页
        :param response:
        :return:
        """
        company_name = response.xpath('//div[@id="content"]//section//h1/text()').extract_first()

        # company_address = response.xpath('string(//section[@id="kontaktdaten"]//li/address)').extract_first()
        # if company_address:
        #     company_address = str(company_address).replace('\t', '').replace('\n', ',').strip(',')
        # print(company_address)

        company_address_list = response.xpath('//section[@id="kontaktdaten"]//li/address/p/text()').extract()
        if company_address_list:
            company_address = ','.join(company_address_list).replace('\t', '').strip()
        else:
            company_address = ''

        company_tel = response.xpath('//section[@id="kontaktdaten"]//li'
                                     '/span[@data-role="telefonnummer"]/@data-suffix').extract_first()

        company_fax = response.xpath('//section[@id="kontaktdaten"]//li'
                                     '/span[@property="faxnumber"]/text()').extract_first()

        company_email = response.xpath('//section[@id="kontaktdaten"]//li'
                                       '/a[@property="email"]/@content').extract_first()

        company_website = response.xpath('//section[@id="kontaktdaten"]//li'
                                         '/a[@property="url"]/@href').extract_first()

        item_dict = {
            'company_name': company_name,
            'company_address': company_address,
            'company_tel': company_tel,
            'company_fax': company_fax,
            'company_email': company_email,
            'company_website': company_website,
        }

        return item_dict
