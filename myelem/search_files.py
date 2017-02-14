#!/usr/bin/env python
# coding=UTF-8
import re
import numpy as np
import patterns
from common import path_define, defines, utils
import numpy as np

class elem_analysis:
    def __init__(self, crime_index):
        self.elemdict = dict(patterns.sp_pattern_dict[defines.crime_list[crime_index]], **patterns.com_pattern_dict)
        self.numelemdict = patterns.sp_num_pattern_dict[defines.crime_list[crime_index]]

    def analysis_sp_elem(self, text):
        sp_elem_dict = {}
        # 记录数值相关要素的值
        for item in self.numelemdict.keys():
            pt_obj = re.compile(patterns.pattern_dict[item][0])
            if item == 'money':
                lst = pt_obj.findall(text)
                if len(lst) > 0:
                    # 取最后一个匹配的结果
                    sp_elem_dict[item] = utils.chn2int(lst[len(lst) - 1])
                else:
                    sp_elem_dict[item] = 0
            elif item == 'count' or item == 'death_count':
                lst = pt_obj.findall(text)
                sp_elem_dict[item] = 0
                if len(lst) > 0:
                    sp_elem_dict[item] = 1
                for it in lst:
                    if it != '':
                        sp_elem_dict[item] = utils.chn2int(it)
            elif item == 'injure_count':
                lst = pt_obj.findall(text)
                qingshang = 0
                zhongshang = 0
                for tup in lst:
                    if tup[1] == u'轻伤':
                        if utils.chn2int(tup[0]) == 0:
                            qingshang = 1
                        else:
                            qingshang = utils.chn2int(tup[0])
                    else:   # 重伤
                        if utils.chn2int(tup[0]) == 0:
                            zhongshang = 1
                        else:
                            zhongshang = utils.chn2int(tup[0])
                sp_elem_dict[item] = (qingshang, zhongshang)
        return sp_elem_dict

    def cmp_sp_elem(self, query_dict, doc_dict):
        doc_score = []
        for item in self.numelemdict.keys():
            score = float(self.numelemdict[item])
            if query_dict[item] == doc_dict[item]:
                doc_score.append(score)
            elif item == 'injure_count':
                if query_dict[item][0] == 0:
                    cur_score = score
                    cur_score -= doc_dict[item][0] * 5
                    cur_score -= abs(query_dict[item][1] - doc_dict[item][1]) * 2
                    doc_score.append(cur_score)
                elif query_dict[item][1] == 0:
                    cur_score = score
                    cur_score -= doc_dict[item][1] * 5
                    cur_score -= abs(query_dict[item][0] - doc_dict[item][0]) * 2
                    doc_score.append(cur_score)
                else:
                    cur_score = score
                    cur_score -= abs(query_dict[item][0] - doc_dict[item][0]) * 2
                    cur_score -= abs(query_dict[item][1] - doc_dict[item][1]) * 2
                    doc_score.append(cur_score)
            else:
                if query_dict[item] == 0:
                    doc_score.append(0)
                else:
                    cur_score = score / (1.0 + abs(query_dict[item] - doc_dict[item]) / query_dict[item])
                    doc_score.append(cur_score)
        return doc_score


    def analysis_com_elem(self, text):
        # 有无类要素，元素即分值
        vec1 = np.zeros((len(self.elemdict)), dtype=float)
        i = 0
        for item in self.elemdict.keys():
            pt_obj = re.compile(item)
            se = pt_obj.search(text)
            if se:
                vec1[i] = self.elemdict[item]
            i += 1
        return vec1


    def analysis_query_text(self, file_name, crime_index):
        f = open(path_define.CRIMINAL_DIR + file_name)
        text = f.read()
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
        ana_inst = elem_analysis(crime_index)
        f = open(path_define.CRIMINAL_DIR + query_filename)
        text = f.read()
        f.close()
        text = text.decode('utf-8')
        pattern = re.compile(u'书.记.员')
        ps = pattern.search(text)
        if ps:
            text = text[:ps.start()]
        print ','.join(ana_inst.elemdict.keys()).encode('utf-8')
        print ','.join(ana_inst.numelemdict.keys()).encode('utf-8')
        qsp_elem = ana_inst.analysis_sp_elem(text)
        qvec = ana_inst.analysis_com_elem(text)
        qvec = np.hstack((qvec, np.array(ana_inst.numelemdict.values())))
        utils.debug_log(query_filename, qvec)
        rst_dict = {}
        for file_name in cmp_file_list:
            f = open(path_define.CRIMINAL_DIR + file_name)
            text = f.read()
            text = text.decode('utf-8')
            pattern = re.compile(u'书.记.员')
            ps = pattern.search(text)
            if ps:
                text = text[:ps.start()]
            dsp_elem = ana_inst.analysis_sp_elem(text)
            dsp_score = ana_inst.cmp_sp_elem(qsp_elem, dsp_elem)
            dvec = ana_inst.analysis_com_elem(text)
            dvec = np.hstack((dvec, dsp_score))
            utils.debug_log(file_name, dvec)
            rst_dict[file_name] = np.linalg.norm(qvec - dvec)
            print 'score=', rst_dict[file_name]
        return rst_dict


