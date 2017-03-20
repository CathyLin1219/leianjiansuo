#! usr/bin/python
# -*- coding:utf-8 -*-

import sys, os
import numpy as np
from common import const_data, metric, xls_parser, utils, path_define
import re

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

def statistic_para(name_list, para_name, dict_name2json):
    '''
    统计平均值和方差
    :param name_list: 案件名列表
    :param para_name: 待统计的参数名
    :param dict_name2json: 案件名与其提取后的json
    :return: 平均值和方差
    '''
    para_values = []
    for name in name_list:
        if name in dict_name2json:
            value = dict_name2json[name][para_name]
            if value != '':
                value = int(value)
            else:
                value = 0
            para_values.append(value)
    print "values of %s are " % para_name
    print para_values
    para_values = np.asarray(para_values)
    mean = np.mean(para_values)
    var = np.var(para_values)
    return mean, var

def similar_case_diff_rst():
    '''
    相似案例统计刑期和罚金的均值和方差，基于已经得到[(case_name1 score1), (case_name2,score2),...] 的pkl数据, 统计结果打印到屏幕
    :return:
    '''
    name2json_dict_pkl = path_define.MAP_NAME2JSON + '.pkl'
    dict_name2json = utils.load_or_calc(name2json_dict_pkl, utils.gen_name2json_dict, \
                                             path_define.MAP_NAME2JSON)
    data_dir = "data/theft_2k_w0.1_0.1_0.4_0.4"
    filelist = os.listdir(data_dir)
    for file in filelist:
        # "%s_gnr_cand_on%d_%s.pkl"
        m = re.search("pkl$" , file)
        if m:
            data = utils.load_pyobj(os.path.join(data_dir, file))  # [(name,score), (name,score), ...]
            m = re.match("[^.]+", file)
            case_name = m.group(0)
            name_list = list(zip(*data)[0])
            mean, var = statistic_para(name_list[:100], 'sentenced_time', dict_name2json)
            print "sentenced_time of %s (mean, var) are %f, %f" % ( case_name, mean, var )
            mean, var = statistic_para(name_list[:100], 'money', dict_name2json)
            print "money of %s (mean, var) are %f, %f" % ( case_name, mean, var )


if __name__ == '__main__':
    #get_my_rank("../data/testcases_1221_0216/theft/")
    similar_case_diff_rst()

