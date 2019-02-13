# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
# import codecs, json  # 自定义导出到json
# from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class MyScrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipeline(object):

    def __init__(self, db_pool):
        self.dbpool = db_pool

    # 项目初始化时候，会先运行这个代码。
    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(host=settings['MYSQL_HOST'],
                       db=settings['MYSQL_DBNAME'],
                       user=settings['MYSQL_USER'],
                       passwd=settings['MYSQL_PASSWORD'],
                       charset='utf8',
                       use_unicode=True,
                       cursorclass=MySQLdb.cursors.DictCursor,
                       )

        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted 让mysql插入变成 异步。
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)

        return item

    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = 'insert into jobbole(front_image_url,front_image_path,' \
                     'url,url_object_id,title,create_date,tags,praise_nums,' \
                     'collection_nums,comments_nums) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(insert_sql, (item['front_image_url'],
                                    item['front_image_path'],
                                    item['url'],
                                    item['url_object_id'],
                                    item['title'],
                                    item['create_date'],
                                    item['tags'],
                                    item['praise_nums'],
                                    item['collection_nums'],
                                    item['comments_nums']
                                    ))


# class MysqlPipeline(object):
#     def __init__(self):
#         self.conn = MySQLdb.connect('localhost',
#                                     'root',
#                                     'huajian',
#                                     'myscrapy',
#                                     charset='utf8',
#                                     use_unicode=True)
#         self.cursor = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         insert_sql = 'insert into jobbole(front_image_url,front_image_path,' \
#                      'url,url_object_id,title,create_date,tags,praise_nums,' \
#                      'collection_nums,comments_nums) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
#         self.cursor.execute(insert_sql, (item['front_image_url'],
#                                          item['front_image_path'],
#                                          item['url'],
#                                          item['url_object_id'],
#                                          item['title'],
#                                          item['create_date'],
#                                          item['tags'],
#                                          item['praise_nums'],
#                                          item['collection_nums'],
#                                          item['comments_nums']
#                                          ))
#         self.conn.commit()
#         return item


# scrapy.exporter中的JsonItemExporter 导出 json 数据。
# class JsonExporterPipeline(object):
#     def __init__(self):
#         self.file = open('article_exporter.json', 'wb')
#         self.exporter = JsonItemExporter(self.file,
#                                          encoding='utf-8',
#                                          ensure_ascii=False)
#         self.exporter.start_exporting()
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
#
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()


# 自定义导出到json
# class JsonPipeline(object):
#     def __init__(self):
#         self.file = codecs.open('article.json', 'w', encoding='utf-8')
#
#     def process_item(self, item, spider):
#         lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
#         self.file.write(lines)
#         return item
#
#     # spider 结束时候，会自动执行这个函数
#     def spider_closed(self, spider):
#         self.file.close()


class JobboleImagePipeline(ImagesPipeline):
    """
    # 下面代码继承ImagesPipeline中的item_completed函数,获取图片下载存储路径
    """

    def item_completed(self, results, item, info):
        front_image_path = results[0][1]['path']
        # front_image_url = results[0][1]['url']
        item['front_image_path'] = front_image_path
        return item
