#!/usr/bin/env python
# coding=UTF-8
import re
import numpy as np
import patterns
from common import path_define, defines, utils
import numpy as np

class elem_analysis:
    def __init__(self, crime_index):
        self.elemdict = dict(patterns.crime_pattern_dict[defines.crime_list[crime_index]], **patterns.com_pattern_dict)
        self.numelemdict = patterns.crime_num_pattern_dict[defines.crime_list[crime_index]]

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
        crime_pattern_list = patterns.crime_pattern_dict[defines.crime_list[crime_index]]
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
        cur_ptlist = patterns.crime_pattern_dict[defines.crime_list[crime_index]] + patterns.com_pattern_list
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

class elem_analyzer:
    '''
    规则匹配查找要素，要素特征计算方法类似F值方式，基于要素存在与否
    '''
    def __init__(self, crime_index):
        crime_pattern_list = patterns.sp_pattern_dict[defines.crime_list[crime_index]]
        self.cur_ptlist = crime_pattern_list + patterns.com_pattern_list

    def analysis_text(self, text):
        elem_arr = np.zeros((len(self.cur_ptlist)), dtype=np.bool)
        for i in range(len(self.cur_ptlist)):
            pt_item = self.cur_ptlist[i]
            pt_obj = re.compile(pt_item)
            m = pt_obj.search(text)
            if m:
                elem_arr[i] = 1
        return elem_arr

    def cmp_elem(self, q_arr, d_arr):
        '''
        使用类似计算F值的方法
        :param q_arr: query 的要素有无向量 0,1 向量
        :param d_arr: document 的要素有无向量
        :return: 2*p*r/(p+r)
        '''
        # query作为正确答案，doc对比q进行计算
        rel_num = float(sum(q_arr))    # number of relevant elements, tp+tn
        retr_num = float(sum(d_arr))    # number of retrival elements, tp+fp
        retr_rel_num = float(sum(q_arr & d_arr))
        if retr_num == 0:
            p = 1
        else:
            p = retr_rel_num / retr_num
        if rel_num == 0:
            r = 1
        else:
            r = retr_rel_num / rel_num
        if (p + r) == 0:
            f = 0
        else:
            f = 2 * p * r / (p + r)
        return f


class ElemRank:
    check_bin_elem_list = ['surrender', 'age_group', 'reconciliation', 'attempt', 'meritorious',
                           'repetitious_theft', 'restitution', 'burglary', 'pickpocket', 'money_group']
    check_value_elem_list = ['amount_of_theft']
    bin_elem_weight = [6, 5, 5, 30, 6,
                       5, 5, 5, 5, 15]
    value_elem_weight = [15]

    def search_as_dict(self, query_filename, crime_index, cmp_file_list):
        ana_inst = elem_analyzer(crime_index)
        f = open(path_define.CRIMINAL_DIR + query_filename)
        query_text = f.read()
        f.close()
        query_text = query_text.decode('utf-8')
        pattern = re.compile(u'书.记.员')
        ps = pattern.search(query_text)
        if ps:
            query_text = query_text[:ps.start()]
        query_arr = ana_inst.analysis_text(query_text.decode('utf8'))
        rst_dict = {}
        for file_name in cmp_file_list:
            f = open(path_define.CRIMINAL_DIR + file_name)
            doc_text = f.read()
            doc_text = doc_text.decode('utf-8')
            pattern = re.compile(u'书.记.员')
            ps = pattern.search(doc_text)
            if ps:
                doc_text = doc_text[:ps.start()]
            doc_arr = ana_inst.analysis_text(doc_text.decode('utf8'))
            grade = ana_inst.cmp_elem(query_arr, doc_arr)
            rst_dict[file_name] = grade
        return rst_dict

    def search_as_dict_0526(self, case_name, uni_list, cand_elem):
        rst_dict = {}
        if case_name in cand_elem:
            elements = cand_elem[case_name]
        else:
            return rst_dict
        for i, doc_name in enumerate(uni_list):
            rst_dict[doc_name], _ = self.cmp_elem(elements, cand_elem[doc_name])
        return rst_dict

    def cmp_elem(self, query, document):
        grade = 0.0
        total = 0.0
        relevant_element = []
        for j in range(0, len(ElemRank.check_bin_elem_list)):
            key = ElemRank.check_bin_elem_list[j]
            if key in query and key in document:
                query_value = query[key]
                document_value = document[key]
                # if isinstance(query_value, bool):
                #     document_value = int(document_value) > 0
                # else:
                #     document_value = document_value.encode("utf8")
                try:
                    query_value = int(query_value)
                    document_value = int(document_value)
                except:
                    query_value = query_value.encode("utf8")
                    document_value = document_value.encode("utf8")
                if query_value or document_value:
                    total += ElemRank.bin_elem_weight[j]
                    if type(query_value) != type(document_value):
                        print "Element %s: query_elem's type and document_elem'type is not same!" % key
                        print "query_elem's type is",type(query_value), "but document_elem'type", type(document_value)
                    elif query_value == document_value:
                        grade += ElemRank.bin_elem_weight[j]
                        relevant_element.append(key)
                    #print "query_elem is", query_value, ",document_elem is", document_value
                else:
                    #print "query_elem is", query_value, ",document_elem is", document_value
                    pass
        for k in range(0, len(ElemRank.check_value_elem_list)):
            key = ElemRank.check_value_elem_list[k]
            if key in query and key in document:
                total += ElemRank.value_elem_weight[k]
                if (isinstance(query[key], int) or isinstance(query[key], float)) and query[key] != 0:
                    query_value = query[key]
                    document_value = float(document[key])
                    grade += abs(query_value - document_value)/(query_value + document_value) * ElemRank.value_elem_weight[k]
                    relevant_element.append(key)
        if total != 0:
            grade = grade / total
        return grade, relevant_element

