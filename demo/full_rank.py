# coding=UTF-8

import pickle, os, sys
from common import path_define, utils, defines, result_handle, statistic
from common.result_handle import ResultHandler
from mylucene.search_files import lucene_rank
from mylda.search_files import lda_rank
from myelem.search_files import ElemRank
from myjudgrst.search_files import judge_rank
from myother.similar_crime import similar_class_crime
import numpy as np

class full_rank:
    def __init__(self):
        name2json_dict_pkl = path_define.MAP_NAME2JSON + '.pkl'
        self.dict_name2json = utils.load_or_calc(name2json_dict_pkl, utils.gen_name2json_dict,\
                                                 path_define.MAP_NAME2JSON)
        self.luc_inst = lucene_rank()
        self.lda_inst = lda_rank(path_define.LDA_MODEL_STR)
        self.elem_inst = ElemRank()
        self.judg_inst = judge_rank(self.dict_name2json)
        #self.sim_inst = similar_class_crime()
        self.result_handler = ResultHandler()


    def data_prepare(self, case_name):
        # 一个案件的数据准备：name, desc, crime_index
        case_desc = self.dict_name2json[case_name]["description"].encode("utf8")
        crime_name = self.dict_name2json[case_name]["criminal_name"]
        crime_index = defines.enum_crime_name(crime_name)
        return case_desc, crime_index


    def general_rank(self, case_name):
        print "Search of %s begin>>>>>>" % case_name
        # 原程序
        case_desc, crime_index = self.data_prepare(case_name)
        utils.debug_log("query description:%s" % case_desc, "criminal index is %d" % crime_index)

        # get lucene result
        top_n = 1000
        luc_cand, cand_elem = self.luc_inst.search_as_dict(case_desc, top_n)
        if case_name in luc_cand:
            luc_cand.pop(case_name)
        utils.normalize_score(luc_cand, True)
        utils.debug_log("lucene search done!")
        utils.debug_log("lucene cand: ", luc_cand)

        # get lda result
        lda_cand = {}
        if defines.FLAG_LDA:
            top_n = 1000
            cur_case_lda_cand_path = path_define.CASE_LDA_CAND_PATH_FMT % (case_name, top_n)
            lda_cand = utils.load_or_calc(cur_case_lda_cand_path, self.lda_inst.search_as_dict, case_desc, top_n)
            if case_name in lda_cand:
                lda_cand.pop(case_name)
            utils.normalize_score(lda_cand, False)
            utils.debug_log("lda search done!")
            utils.debug_log("lda cand: ", lda_cand)

        # union of lucene + lda + random_of_similar_crime
        uni_list = list(set(luc_cand.keys()).union(set(lda_cand.keys())))   # Lucene U LDA
        utils.debug_log("lucene + lda union size = ", len(uni_list))

        # 对于基本候选集进行附加操作
        # self.accessory_process(uni_list, crime_index)

        # calc element result
        elem_cand = {}
        elem_cand_0526 = {}
        if defines.FLAG_ELEM:
            elem_cand = self.elem_inst.search_as_dict(case_name, crime_index, uni_list)
            elem_cand_0526 = self.elem_inst.search_as_dict_0526(case_name, uni_list, cand_elem)
            # cur_case_elem_cand_path = path_define.CASE_ELEM_CAND_PATH_FMT % (case_name, len(uni_list))
            # elem_cand = utils.load_or_calc(cur_case_elem_cand_path, self.elem_inst.search_as_dict,
            #                                case_name, crime_index, uni_list)
            statistic.statistic_elem_rst(elem_cand, elem_cand_0526)

        # calc judge result similarity
        judg_cand = {}
        if defines.FLAG_JUDG:
            cur_case_judg_cand_path = path_define.CASE_JUDG_CAND_PATH_FMT % (case_name, len(uni_list))
            judg_cand = utils.load_or_calc(cur_case_judg_cand_path, self.judg_inst.search_as_dict,
                                           case_name, uni_list)

        # calc court revelence
        # cur_case_court_cand_path = path_define.CASE_JUDG_CAND_PATH_FMT % (case_name, len(uni_list))
        # court_cand = utils.load_or_calc(cur_case_court_cand_path, self.judg_inst.search_as_dict,
        #                                case_name, uni_list)

        # 加权求和
        feature_weight = [defines.LUCENE_RATE, defines.LDA_RATE, defines.ELEM_RATE, defines.JUDG_RATE]
        score_sum_list = self.weighted_sum(luc_cand, lda_cand, elem_cand_0526, judg_cand,
                                           full_name_list=uni_list, weights_list=feature_weight)
        rank_pairs = self.sort_score(uni_list, score_sum_list)


        # # 附加操作
        # 1.统计来源
        #self.result_handler.analyze_luc_vs_lda(luc_cand, lda_cand, rank_pairs)
        # 2.生成人工评级的文本
        self.result_handler.save_for_human_rating(case_name, rank_pairs, 30)

        # 保存结果，文件名及得分
        general_result_path = path_define.CASE_GENERAL_CAND_PATH_FMT % (case_name, len(uni_list),
                                                                        '_'.join(map(str, feature_weight)))
        utils.dump_pyobj(rank_pairs, general_result_path)
        save_final_path = path_define.CASE_GENERAL_CAND_LIST_PATH_FMT % (case_name, len(uni_list),
                                                                         '_'.join(map(str, feature_weight)))
        self.result_handler.save_rst_list(rank_pairs, save_final_path)
        # self.save_rst(general_result_path)
        self.result_handler.measure_with_testcase(case_name, rank_pairs)

    def weighted_sum(self, *arg, **kwargs):
        """
        多个特征的得分，先归一化，再加权求和
        :param arg: 多个特征的得分结果词典，key为文件名，value为得分
        :param kwargs:
                    full_name_list= (必须)：全部相似候选的文件名列表
                    weights_list= (必须)：各特征的权值，必须与输入的arg中的dict顺序对应
        :return:
        """
        full_name_list = kwargs["full_name_list"]
        weights_list = kwargs["weights_list"]
        # 行为doc， 列为特征
        cand_len = len(full_name_list)
        cand_cnt = len(arg)
        score_matrix = np.zeros((cand_len, cand_cnt), np.float)
        utils.debug_log("score_matrix shape is ", score_matrix.shape)
        # 因为可能存在有的排序方法对应的文档不在top，则以该方面的最低分计算
        j = 0
        while j < cand_cnt:
            if len(arg[j]) > 0:
                min_value = min(arg[j].values())
                score_matrix[:, j] = min_value
            j += 1
        i = 0
        while i < cand_len:
            j = 0
            while j < cand_cnt:
                if full_name_list[i] in arg[j]:
                    score_matrix[i,j] = arg[j][full_name_list[i]]
                j += 1
            i += 1
        score_sum_array = np.sum(score_matrix * weights_list, axis=1)
        utils.debug_log("after weighted sum, array shape is ", score_sum_array.shape)
        return score_sum_array


    def sort_score(self, name_list, score_list):
        dec_index = np.argsort(-score_list)  # 降序排列
        name_list = np.array(name_list)
        return zip(name_list[dec_index], score_list[dec_index])

    def save_rst(self, rst_pkl):
        self.result_handler.save_rst_report(rst_pkl, self.dict_name2json)

    def accessory_process(self, cand_list, crime_index = -1):
        '''
        1. 过滤非相近罪名案例
        :param cand_list:
        :param crime_index:
        :return:
        '''
        # 过滤非相近罪名
        if crime_index in defines.confused_crime.keys():
            sim_crim_set = set(defines.confused_crime[crime_index] + [crime_index])
            i = 0
            while i < len(cand_list):
                cur_index = defines.enum_crime_name(cand_list[i].get('criminal_name'))
                if cur_index not in sim_crim_set:
                    print "delete %d criminal is %s" % (i, cand_list[i].get('criminal_name'))
                    del cand_list[i]
                    continue
                i += 1

