#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright (C)2018 SenseDeal AI, Inc. All Rights Reserved
Author: xuwei
Email: weix@sensedeal.ai
Description:
'''

from elasticsearch_dsl import Document, Keyword, Text, Float, Nested, Date, Integer
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search, Q
from elasticsearch.helpers import bulk
from .config_log import config


class OtherName(Document):
    company_code = Keyword()
    other_name = Text(analyzer='ik_max_word')
    company_full_name = Text(analyzer='ik_max_word')

    class Index:
        name = 'other_name'
        using = 'es'

    def save(self, **kwargs):
        return super(OtherName, self).save(**kwargs)


def get_es_client(label='', host='', user='', password=''):
    if label:
        host = config(label, 'host')
        user = config(label, 'user', '')
        password = config(label, 'pass', '')
    else:
        host = host
        user = user
        password = password
        label = 'default'
    if user and password:
        return connections.create_connection(alias=label, hosts=[host], http_auth=(user, password), timeout=300)
    return connections.create_connection(alias=label, hosts=[host], timeout=300)


class EsOp(object):
    def __init__(self, index, label='', host='', user='', password='', size=2000):
        self.conn = get_es_client(label=label, host=host, user=user, password=password)
        self.index = index
        self.size = size

    def get_es_state(self):
        print(self.conn.cluster.state())
        print(self.conn.cluster.health())

    def get_es_info(self):
        return self.conn.info()

    # 解决es写入立刻查找查询不到的问题
    def refresh_index(self, index=None, **kwargs):
        self.conn.indices.refresh(index=index, **kwargs)

    def get_indices_info(self):
        return self.conn.cat.indices(format='json')

    def get_index_details(self, index):
        return self.conn.indices.get(index=index)

    def get_mapping_details(self, index):
        return self.conn.indices.get_mapping(index=index)

    def get_index_fields_infos(self, index, fields: list, **kwargs):
        return self.conn.indices.get_field_mapping(index=index, fields=fields, **kwargs)

    def delete_index(self):
        self.conn.indices.delete(self.index, ignore=[400, 404])

    def delete_by_id(self, id, **kwargs):
        self.conn.delete(index=self.index, id=id, ignore=[400, 404], **kwargs)

    def set_alias(self, other_name):
        self.conn.indices.put_alias(index=self.index, name=other_name)

    def delete_alias(self, other_name):
        self.conn.indices.delete_alias(index=self.index, name=other_name, ignore=[400, 404])

    def add_one_data(self, body, id=None, **kwargs):
        self.conn.index(index=self.index, body=body, id=id, **kwargs)

    def __query_iterator(self, query, scroll='1m'):
        iter_item = self.__query_iterator_origin(query, scroll=scroll)
        for item in iter_item:
            item["hits"] = [_obj['_source'] for _obj in item["hits"]]
            yield item

    def __query_iterator_origin(self, query, scroll='1m'):
        total = query['hits']['total']['value']  # es查询出的结果总量
        scroll_id = query['_scroll_id']  # 游标用于输出es查询出的所有结果
        hits = query['hits']['hits']
        num = len(hits)
        yield {"total": total, "num": num, "scroll_id": scroll_id, "hits": hits}

        for i in range(0, int(total / self.size)):
            # scroll参数必须指定否则会报错
            scroll_query = self.conn.scroll(scroll_id=scroll_id, scroll=scroll)
            hits = scroll_query['hits']['hits']
            scroll_id = scroll_query['_scroll_id']
            num += len(hits)
            yield {"total": total, "num": num, "scroll_id": scroll_id, "hits": hits}

        # 清除滚动查询的状态，释放相关资源
        self.conn.clear_scroll(scroll_id=scroll_id)

    def get_query_iterator(self, body, scroll='1m', **kwargs):
        """
        :param body: es查询字典
        :param scroll: 游标未被使用过期时间
        :param kwargs:
        :return: {"total": total, "num": num,  "scroll_id": scroll_id, "hits": hits}
        """
        iter_item = self.get_query_iterator_origin(body, scroll=scroll, **kwargs)
        for item in iter_item:
            item["hits"] = [_obj['_source'] for _obj in item["hits"]]
            yield item

    def get_query_iterator_origin(self, body, scroll="1m", **kwargs):
        """
        :param body: es查询字典
        :param scroll: 游标未被使用过期时间
        :param kwargs:
        :return: {"total": total, "num": num,  "scroll_id": scroll_id, "hits": hits}
        """
        query = self.conn.search(
            index=self.index, body=body, scroll=scroll, size=self.size, ignore=[400, 404], **kwargs)
        return self.__query_iterator_origin(query, scroll=scroll)

    def es_query(self, body, **kwargs):
        _data = self.conn.search(index=self.index, body=body, ignore=[400, 404], size=self.size, **kwargs)
        return _data

    def get_one_data(self, id, **kwargs):
        _data = self.conn.get(index=self.index, id=id, ignore=[400, 404], **kwargs)
        return _data

    def update_one_data(self, id, body=None, **kwargs):
        self.conn.update(index=self.index, id=id, body=body, **kwargs)

    # 查询field="python"或"android"的所有数据
    # term_name = {"field": ["python", "android"]}
    def terms_query(self, term_name, **kwargs):
        _body = {'query': {'term': term_name}, 'size': 10, 'from': 0}
        _data = self.conn.search(index=self.index, body=_body, **kwargs)
        return _data

    # term_name = {"field": ["python", "android"]}field包含python关键字的数据
    def match_query(self, term_name, **kwargs):
        # match:匹配name包含python关键字的数据
        _body = {'query': {'match': term_name}, 'size': 10}
        _data = self.conn.search(index=self.index, body=_body, **kwargs)
        return _data

    # 多个字段其一含有某个字符
    # term_name = {"query": "深圳", "fields": ["name", "addr"]}
    def multi_match(self, term_name, **kwargs):
        _body = {'query': {'multi_match': term_name}, 'size': 10}
        _data = self.conn.search(index=self.index, body=_body, **kwargs)
        return _data

    def bulk_to_es(self, bulk_list, **kwargs):
        _length = len(bulk_list)
        if _length > 100:
            for i in range(0, _length, 100):
                bulk(self.conn, bulk_list[i: i + 100], index=self.index, **kwargs)
        else:
            bulk(self.conn, bulk_list, index=self.index, **kwargs)

