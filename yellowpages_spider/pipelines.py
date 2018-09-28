# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class YellowpagesSpiderPipeline(object):
    """
    pipeline
    """
    def __init__(self):
        self.fp = None
        self.company_list = list()

    def process_item(self, item, spider):
        self.company_list.append(item)
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        with open(fr'./yellowpages_spider/data/{spider.name}.json', 'w', encoding='utf8') as fp:
            fp.write(json.dumps(self.company_list))
