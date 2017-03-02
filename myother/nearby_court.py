# coding=UTF-8

from pymongo import MongoClient
from common import utils
import numpy as np

grade_score = np.power(2, np.arange(0, 4))

class analyz_court:
    def __init__(self, mongodb_uri, db_name, dict_name2json):
        '''
        连接数据库
        :param mongodb_uri: 数据库连接URI
        :param db_name: 数据库名称
        '''
        client = MongoClient(mongodb_uri) # 'mongodb://localhost:27017/'
        self.db = client[db_name]
        self.dict_name2json = dict_name2json


    def find_coll(self, collection_name, condition, query):
        '''
        从集合中进行查询，返回查询结果
        :param collection_name: 集合名
        :param condition: 查询条件，{ <field1>: <value1>, <field2>: <value2>, ... }
        :param query: 查询返回域，{ <field1>: 1, <field2>: 0, ... }
        :return:
        '''
        collection = self.db[collection_name]
        rst_docs = []
        cursor = collection.find(condition, query)
        for doc in cursor:
            rst_docs.append(doc)
        return rst_docs

    def get_court_seq(self, court_name):
        '''
        Todo
        :param court_name:
        :return:
        '''
        cid = utils.get_md5(court_name)
        condition_fmt = '{"_id":%s}'
        query = '{"superior":1, "level":1, "_id": 0}'
        cursor = self.find_coll('court', condition_fmt % cid, query)
        if cursor.count() < 1:
            return []
        sup = cursor[0]['superior']
        level = cursor[0]['level']
        seq = [None, None, None]
        seq[level-1] = cid



    def cmp_court(self, query_court, doc_court):
        if not query_court.strip() or not doc_court.strip():
            return 0
        # 同法院，等级最高
        if query_court == doc_court:
            return 3

        # 有共同的上级，或互为上下级，各自与他们的上级做集合，一定有重合项，则数量<=3
        qc_id = utils.get_md5(query_court)
        dc_id = utils.get_md5(doc_court)
        condition = {"_id":''}
        query = {"superior":1, "level":1, "_id": 0}
        condition['_id'] = qc_id
        qrst_cursor = self.find_coll('court', condition, query)
        condition['_id'] = dc_id
        drst_cursor = self.find_coll('court', condition, query)
        if len(qrst_cursor) < 1 or len(drst_cursor) < 1:  # 都能查询到结果
            return 0
        q_sup = qrst_cursor[0]['superior']
        d_sup = drst_cursor[0]['superior']
        q_level = qrst_cursor[0]['level']
        d_level = drst_cursor[0]['level']
        court_set = set([qc_id, dc_id, q_sup, d_sup])
        # q,d不能同时为高级法院，否则一定成立
        if len(court_set) <= 3:
            if q_level < 3 or d_level < 3:
                return 2
            else:
                return 0

        # 有共同的上上级，或a上级=b上上级，且其中一个必为基层法院，上上级同为最高法没有意义
        condition['_id'] = q_sup
        qrst_cursor = self.find_coll('court', condition, query)
        condition['_id'] = d_sup
        drst_cursor = self.find_coll('court', condition, query)
        if len(qrst_cursor) < 1 or len(drst_cursor) < 1:  # 都能查询到结果
            return 0
        q_ssup = qrst_cursor[0]['superior']
        d_ssup = drst_cursor[0]['superior']
        court_set = court_set.union(set([q_ssup,d_ssup]))
        # q,d不能同时为高级法院，否则一定成立
        if len(court_set) <= 5:
            if q_level == 1 or d_level == 1:
                return 1
            else:
                print '101'
                return 0

        # 其他没有交叉法院
        print '105'
        return 0

    def analyze_court(self, query_filename, cmp_file_list):
        rst_dict={}
        if query_filename not in self.dict_name2json:
            return rst_dict
        q_court = self.dict_name2json[query_filename]["court"]
        for file_name in cmp_file_list:
            if file_name in self.dict_name2json:
                doc_court = self.dict_name2json[file_name]["court"]
                grade = self.cmp_court(q_court, doc_court)
                rst_dict[file_name] = grade_score[grade]
            else:
                rst_dict[file_name] = grade_score[0]
        return rst_dict

if __name__ == '__main__':
    inst = analyz_court('mongodb://localhost:27017/','justice', None)
    print inst.cmp_court('东京城林区基层法院', '东京城林区基层法院')
    print 'expected: 3'
    print '============='
    print inst.cmp_court('东京城林区基层法院','东方红林区基层法院')
    print 'expected: 2'
    print '============='
    print inst.cmp_court('东京城林区基层法院', '黑龙江省林区中级人民法院')
    print 'expected: 2'
    print '============='
    print inst.cmp_court('东京城林区基层法院', '黑龙江省高级人民法院')
    print 'expected: 1'
    print '============='
    print inst.cmp_court('东京城林区基层法院', '吉林省延边林区中级法院')
    print 'expected: 0'
    print '============='
    print inst.cmp_court('东京城林区基层法院', '最高人民法院')
    print 'expected: 0'
    print '============='