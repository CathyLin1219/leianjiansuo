#!/usr/bin/env python
# coding=UTF-8
import sys, subprocess, os, re
import numpy as np
import patterns
from common import path_define, defines


class elem_analysis:
    def __init__(self):
        pass

    def analysis_query_text(self, file_name, crime_index):
        f = open(path_define.CRIMINAL_DIR + file_name)
        text = f.read() #.decode('utf8')
        f.close()
        crime_pattern_list = patterns.sp_pattern_dict[defines.crime_list[crime_index]]
        cur_ptlist = crime_pattern_list + patterns.com_pattern_list
        elem_cnt = len(cur_ptlist)
        elem_vec = ['' for i in range(elem_cnt)]
        i = 0
        for pt_item in cur_ptlist:
            pt_obj = re.compile(pt_item)
            lst = pt_obj.findall(text)
            if len(lst) > 0:
                #print len(lst)
                # 取最后一个匹配的结果
                elem_vec[i] = lst[len(lst) - 1]
            i += 1

        return elem_vec

    def cmp_text_elem(self, cmp_file_name, q_vec, crime_index):
        f = open(path_define.CRIMINAL_DIR + cmp_file_name)
        cmp_text = f.read()  # .decode('utf8')
        f.close()
        cur_ptlist = patterns.sp_pattern_dict[defines.crime_list[crime_index]] + patterns.com_pattern_list
        q_elem_cnt = 0
        cmp_elem_cnt = 0
        i = 0
        while i < len(cur_ptlist):
            if q_vec[i] != '':
                q_elem_cnt += 1
                pt_obj = re.compile(cur_ptlist[i])
                lst = pt_obj.findall(cmp_text)
                if len(lst) > 0:
                    cmp_elem_cnt += 1
            i += 1
        return q_elem_cnt and float(cmp_elem_cnt)/q_elem_cnt or 0

class elem_rank:
    def search_as_dict(self, query_filename, crime_index, cmp_file_list):
        ana_inst = elem_analysis()
        query_vec = ana_inst.analysis_query_text(query_filename, crime_index)
        i = 0
        rst_dict = {}
        for file_name in cmp_file_list:
            rst_dict[file_name] = ana_inst.cmp_text_elem(file_name, query_vec, crime_index)
            #print "file=", file_name, "score=", rst_dict[file_name]
            i += 1
        return rst_dict


