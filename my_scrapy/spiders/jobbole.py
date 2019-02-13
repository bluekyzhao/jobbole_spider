# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from scrapy.http import Request
# 希望使用urljoin函数
from urllib.parse import urljoin
from my_scrapy.items import JobboleArticleItem
from my_scrapy.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['jobbole.com']
    # http://blog.jobbole.com/all-posts/
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        # 获取每篇文章的URL并交给具体解析函数
        # 获取下一页的URL并且交给scrapy进行解析
        """

        url_nodes = response.css('div#archive div.post.floated-thumb')
        for node in url_nodes:
            post_url = node.css('a.archive-title::attr(href)').extract_first()
            image_url = node.css('img::attr(src)').extract_first()
            yield Request(url=urljoin(response.url, post_url),
                          callback=self.parse_detail,
                          meta={'front_image_url': image_url})

        next_url = response.css('a.next.page-numbers::attr(href)').extract()[0]
        if next_url:
            yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        """
        # 解析详细文章
        title : 题目
        create_date : 文章发布日期
        praise_nums ： 点赞数
        collection_nums ： 收藏数
        comments_nums ： 评论数
        """
        # 实例化
        article_item = JobboleArticleItem()

        front_image_url = response.meta.get('front_image_url')
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        title = response.css('div.entry-header h1::text').extract()[0]
        entry_meta = response.xpath('//div[@class="entry-meta"]')
        create_date = entry_meta.xpath('p[1]/text()').extract()[0].replace("·", "").strip()
        # create_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].replace('·', '').strip()
        other_meta_list = entry_meta.xpath('p[1]/a/text()').extract()
        tags = ' - '.join(other_meta_list)
        # other_meta_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()

        # =====================================================================
        post_adds = response.xpath('//div[@class="post-adds"]')
        # post_adds = response.css('div.post-adds')

        praise_str = post_adds.css('h10::text').extract()[0]

        collection_str = post_adds.xpath('span[2]/text()').extract()[0]

        comments_str = post_adds.xpath('a/span/text()').extract()[0]

        # =====================================================================

        entry = response.xpath('//div[@class="entry"]').extract()[0]

        # ========================================================================

        # 下载图片要用list传过去
        article_item['front_image_url'] = [front_image_url]
        # front_image_path  在pipeline中得到
        article_item['url'] = response.url
        article_item['url_object_id'] = get_md5(response.url)
        article_item['title'] = title
        try:
            create_date = datetime.strptime(create_date, "%Y/%m/%d").date()
        except:
            create_date = datetime.now().date()
        article_item['create_date'] = create_date
        article_item['tags'] = tags
        article_item['praise_nums'] = praise_str
        article_item['collection_nums'] = collection_str
        article_item['comments_nums'] = comments_str
        # article_item['entry'] = entry

        yield article_item
