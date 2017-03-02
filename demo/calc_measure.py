#! usr/bin/python
# -*- coding:utf-8 -*-

import sys, os
import numpy as np
from common import const_data, metric, xls_parser

reload(sys)
sys.setdefaultencoding('utf-8')

def fabao_measure(cand_dict, k):
    measures_rst = {}
    for key in cand_dict:
        cur_rank_list = np.array(cand_dict[key]) - 1
        dcg_k = metric.dcg_at_k(cur_rank_list, k)
        ndcg_k = metric.get_ndcg(cur_rank_list, k)
        measures_rst[key] = (dcg_k, ndcg_k)
    return measures_rst

def get_fabao_rank():
    print fabao_measure(const_data.fabao_kill_dict, 10)
    print fabao_measure(const_data.fabao_kill_dict, 5)
    print fabao_measure(const_data.fabao_kill_dict, 3)
    print fabao_measure(const_data.fabao_kill_dict, 1)

    print fabao_measure(const_data.fabao_theft_dict, 10)
    print fabao_measure(const_data.fabao_theft_dict, 5)
    print fabao_measure(const_data.fabao_theft_dict, 3)
    print fabao_measure(const_data.fabao_theft_dict, 1)

def get_my_rank(dir):
    xls_list = os.listdir(dir)
    rank_dict = {}
    for doc in xls_list:
        path = os.path.join(dir,doc)
        rating_file, cur_rating = xls_parser.get_hm_rating_xls(path)
        cur_rating = np.array(cur_rating) - 1
        rank_dict[rating_file] = [metric.dcg_at_k(cur_rating, 10), metric.get_ndcg(cur_rating, 10),
                                  metric.dcg_at_k(cur_rating, 5), metric.get_ndcg(cur_rating, 5),
                                  metric.dcg_at_k(cur_rating, 3), metric.get_ndcg(cur_rating, 3),
                                  metric.dcg_at_k(cur_rating, 1), metric.get_ndcg(cur_rating, 1), ]
    print rank_dict




if __name__ == '__main__':
    get_my_rank("../data/testcases_1221_0216/theft/")

