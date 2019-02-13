# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobboleArticleItem(scrapy.Item):
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()  # 在pipeline中得到

    url = scrapy.Field()
    url_object_id = scrapy.Field()    # 在pipeline中得到

    title = scrapy.Field()

    create_date = scrapy.Field()
    tags = scrapy.Field()
    praise_nums = scrapy.Field()
    collection_nums = scrapy.Field()
    comments_nums = scrapy.Field()
    # entry = scrapy.Field()
