#!/usr/bin/env python
# coding=UTF-8
import sys, subprocess, re, os
from common import defines, utils

class judge_rank:
    def __init__(self, dict_name2json):
        self.dict_name2json = dict_name2json


    def search_as_dict(self, query_filename, cmp_file_list):
        query_tump = self.get_judge(query_filename)
        i = 0
        rst_dict = {}
        for file_name in cmp_file_list:
            doc_tump = self.get_judge(file_name)
            rst_dict[file_name] = self.simi_analyze(query_tump, doc_tump)
            utils.debug_log("%d/%d" % (i, len(cmp_file_list)))
            i += 1
        return rst_dict

    def get_judge(self, filename):
        cri_index = defines.enum_crime_name(self.dict_name2json[filename]["criminal_name"])
        sent_time = self.dict_name2json[filename]["sentenced_time"]
        money = self.dict_name2json[filename]["money"]
        if type(sent_time) != int:
            sent_time = 0
        if money == '':
            money = 0
        else:
            money = int(money)
        return cri_index, sent_time, money

    def simi_analyze(self, query_rst, doc_rst):
        score = 0.0
        # criminal name
        if doc_rst[0] == query_rst[0]:
            score += 50.0
        elif doc_rst[0] in defines.confused_crime[query_rst[0]]:
            score += 40.0
        else:
            return score
        # 刑期
        if query_rst[1] != 0:
            score += 30.0 * (1.0 - float(abs(query_rst[1] - doc_rst[1])) / query_rst[1])
        elif doc_rst[1] == 0:
            score += 30.0
        # 罚金
        if query_rst[2] != 0:
            score += 20.0 * (1.0 - float(abs(query_rst[2] - doc_rst[2])) / query_rst[2])
        elif doc_rst[2] == 0:
            score += 20.0
        return score
