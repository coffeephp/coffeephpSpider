# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import time
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi

logger = logging.getLogger('coffeephp')

class CoffeephpspiderPipeline(object):
    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            port=settings['MYSQL_PORT'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbargs)
        return cls(dbpool)

    def __init__(self, dbpool):
        self.dbpool = dbpool

    # pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._conditional_insert, item, spider)  # 调用插入的方法
        d.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        d.addBoth(lambda _: item)
        return d

    def _conditional_insert(self, conn, item, spider):
        if len(item['url']) == 0 or len(item['title']) == 0:
            pass

        if spider.name == 'juejin':
            domain = 'https://juejin.im'
        elif spider.name == 'segmentfault':
            domain = 'https://segmentfault.com'
        elif spider.name == 'toutiao':
            domain = 'https://toutiao.io'
        else:
            domain = ''
            pass

        url = item['url'][0]
        title = item['title'][0]

        if url[0] == '/':
            url = domain + url

        bodyOriginal = '分享链接 [' + url + '](' + url + ')'
        body = '<p>分享链接 <a href="' + url + '">' + url + '</a></p>'

        logger.info('title:' + title)
        logger.info('url:' + url)

        # 查重处理
        conn.execute(
            "select title, url from shares where url = %s or title = %s",
            (url, title))
        # 是否有重复数据
        repetition = conn.fetchone()

        # 重复
        if repetition:
            pass
        else:
            now_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            conn.execute("insert into shares (users_id, title, url, clicks, created_at, updated_at) values (%s, %s, %s, %s, %s, %s)",
                     ('1', title, url, '0', now_datetime, now_datetime))
            conn.execute(
                "insert into topics (users_id, categories_id, title, body_original, body, created_at, updated_at) values (%s, %s, %s, %s, %s, %s, %s)",
                ('1', '2', title, bodyOriginal, body, now_datetime, now_datetime))

    def _handle_error(self, failue, item, spider):
        print(failue)