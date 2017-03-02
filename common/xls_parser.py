#! usr/bin/python
# -*- coding:utf-8 -*-

import sys, json, os
import xlrd

reload(sys)
sys.setdefaultencoding('utf-8')

def get_hm_rating_xls(xls_path):
    '''
    excel中获取rank列表
    数据格式为：第一列第二行为检索文书名，第二列为被检索文书的人工评价等级
    :param xls_path:
    :return: query_filename, [lable1, lable2, ...]
    '''
    # 打开excel
    data = xlrd.open_workbook(xls_path)
    # 得到第一个工作表，或者通过索引顺序 或 工作表名称
    table = data.sheets()[0]
    # 获取第二列的值（数组），评价等级在第二列
    rating_file = table.cell(1, 0).value
    b_col = table.col_values(1)
    hm_ratings = []
    for i in range(1, len(b_col)):
        if type(b_col[i]) == type(1.0):
            hm_ratings.append(int(b_col[i]))
    return rating_file, hm_ratings


def get_qdls(xls_path):
    '''
    excel获取 query， documents 及它们对应的lable
    一个excel为一个query及它的被检索文书
    :param xls_path: 单个excel路径
    :return: doc1:lable1, doc2:lable2, ...
    '''
    # 打开excel
    data = xlrd.open_workbook(xls_path)
    # 得到第一个工作表，或者通过索引顺序 或 工作表名称
    table = data.sheets()[0]
    rating_file = table.cell(1, 0).value
    # 组成A-B列的 <文件名：等级> 键值对
    a_col = table.col_values(0)
    b_col = table.col_values(1)
    hm_ratings = {}
    for i in range(1, len(b_col)):
        if type(b_col[i]) == type(1.0):
            hm_ratings[str(a_col[i])] = int(b_col[i])
    return rating_file, hm_ratings


def get_testcase_lables(dir):
    '''
    读取目录中的excel文本，格式化读入query-documents-lable的数据
    :param dir:
    :return: {query1:{doc1: lable1, doc2: lable2, ...}, query2: {doc1: lable1, ...}, ...}
    '''
    xls_list = os.listdir(dir)
    testcase_dict = {}
    for doc in xls_list:
        path = os.path.join(dir, doc)
        rating_file, cur_rating = get_qdls(path)
        testcase_dict[rating_file] = cur_rating
    return testcase_dict