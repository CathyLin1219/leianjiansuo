#! usr/bin/python
# -*- coding:utf-8 -*-

import sys, os
import numpy as np
from common import const_data, metric, xls_parser, utils, path_define
import re, json

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
    case_dict = {}
    avg_dcg10 = 0
    avg_dcg5 = 0
    avg_dcg3 = 0
    avg_dcg1 = 0
    for doc in xls_list:
        path = os.path.join(dir,doc)
        #print path
        rating_file, cur_rating = xls_parser.get_hm_rating_xls(path)
        cur_rating = np.array(cur_rating[:20]) - 1
        #print rating_file, cur_rating.shape
        dcg10 = metric.dcg_at_k(cur_rating, 10)
        dcg5 = metric.dcg_at_k(cur_rating, 5)
        dcg3 = metric.dcg_at_k(cur_rating, 3)
        dcg1 = metric.dcg_at_k(cur_rating, 1)
        case_dict[rating_file] = {}
        case_dict[rating_file]['dcg10'] = dcg10 #metric.get_ndcg(cur_rating, 10),
        case_dict[rating_file]['dcg5'] = dcg5  #metric.get_ndcg(cur_rating, 5),
        case_dict[rating_file]['dcg3'] = dcg3 #metric.get_ndcg(cur_rating, 3),
        case_dict[rating_file]['dcg1'] = dcg1 #metric.get_ndcg(cur_rating, 1),
        avg_dcg10 += dcg10
        avg_dcg5 += dcg5
        avg_dcg3 += dcg3
        avg_dcg1 += dcg1

    rst_dict = {}
    if len(xls_list) > 0:
        rst_dict['avg_dcg10'] = avg_dcg10 / len(xls_list)
        rst_dict['avg_dcg5'] = avg_dcg5 / len(xls_list)
        rst_dict['avg_dcg3'] = avg_dcg3 / len(xls_list)
        rst_dict['avg_dcg1'] = avg_dcg1 / len(xls_list)
        rst_dict['all_cases'] = case_dict
    return rst_dict

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


def cmp_sys_rst(case_dict1, case_dict2):
    '''
    比较两个方法得到的相同query的打分结果
    :param case_dict1:
    :param case_dict2:
    :return:
    '''
    total_cnt = 0
    grater_cnt = 0
    dcg10_grater_cnt = 0
    dcg5_grater_cnt = 0
    dcg3_grater_cnt = 0
    dcg1_grater_cnt = 0
    for key_case in case_dict1:
        if key_case in case_dict2:
            total_cnt += 1
            case1_score = case_dict1[key_case]['dcg10'] + case_dict1[key_case]['dcg5'] + case_dict1[key_case]['dcg3'] + case_dict1[key_case]['dcg1']
            case2_score = case_dict2[key_case]['dcg10'] + case_dict2[key_case]['dcg5'] + case_dict2[key_case]['dcg3'] + case_dict2[key_case]['dcg1']
            #print key_case,'\t', case1_score, '\t',case2_score
            if case1_score > case2_score:
                 grater_cnt += 1
            if case_dict1[key_case]['dcg10'] > case_dict2[key_case]['dcg10']:
                dcg10_grater_cnt += 1
            if case_dict1[key_case]['dcg5'] > case_dict2[key_case]['dcg5']:
                dcg5_grater_cnt += 1
            if case_dict1[key_case]['dcg3'] > case_dict2[key_case]['dcg3']:
                dcg3_grater_cnt += 1
            if case_dict1[key_case]['dcg1'] > case_dict2[key_case]['dcg1']:
                dcg1_grater_cnt += 1
    if total_cnt <= 0:
        print 'two system result have no same cases'
        return -1
    return float(grater_cnt) / total_cnt, \
           float(dcg10_grater_cnt) / total_cnt, \
           float(dcg5_grater_cnt) / total_cnt,\
           float(dcg3_grater_cnt) / total_cnt,\
           float(dcg1_grater_cnt) / total_cnt

def load_dir_rank_save(dir):
    rank_rst = get_my_rank("data/testcases/%s/" % dir)
    file = open('data/testcases/%s.json' % dir, 'w')
    file.write(json.dumps(rank_rst, ensure_ascii=False))
    file.close()
    return rank_rst


# 命令行参数：保存文件名
if __name__ == '__main__':
    le_new_dir = 'testcases_lucene_elem_0609_theft'
    le_new_rst = load_dir_rank_save(le_new_dir)
    # full_rank_dir = 'testcases_lucene_lda_elem_orirst_1221_theft'
    # full_rst = load_dir_rank_save(full_rank_dir)
    lucene_elem_rank_dir = 'testcases_lucene_elem_0526_theft'
    le_rst = load_dir_rank_save(lucene_elem_rank_dir)
    # lucene_rank_dir = 'testcases_lucene_only_0306-theft'
    # lo_rst = load_dir_rank_save(lucene_rank_dir)
    # print 'full > lucene+elem percent:', cmp_sys_rst(full_rst['all_cases'], le_rst['all_cases'])
    # print 'lucene+elem > lucene percent:', cmp_sys_rst(le_rst['all_cases'], lo_rst['all_cases'])
    # print 'full > lucene percent:', cmp_sys_rst(full_rst['all_cases'], lo_rst['all_cases'])
    print 'new lucene+elem > lucene+elem:', cmp_sys_rst(le_new_rst['all_cases'], le_rst['all_cases'])
    #similar_case_diff_rst()

