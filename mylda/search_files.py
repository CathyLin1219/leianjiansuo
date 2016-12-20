#!/usr/bin/env python
# coding=utf8

import sys, os.path, subprocess
from datetime import datetime
import numpy as np
import numpy.linalg as la
from common import path_define, utils


class lda_rank:
    def __init__(self, model_str):
        sample_name_file = open(path_define.LDA_MODEL_SAMPLE_NAME_FILE, 'r')
        self.sample_name_list = sample_name_file.read().split('\n')
        sample_name_file.close()

        self.model_str = model_str
        # 构造data2, M*K 矩阵
        sample_theta_path = path_define.DATA_DIR + self.model_str + ".theta"
        sample_theta_npy = sample_theta_path + ".npy"
        if os.path.isfile(sample_theta_npy):
            self.data2 = np.load(sample_theta_npy)
        else:
            sfile = open(sample_theta_path, "r")
            sample_docs = sfile.readlines()
            sfile.close()
            self.data2 = np.zeros((len(sample_docs), len(sample_docs[0].split())))
            i = 0
            for sample_doc in sample_docs:
                vec2_str = sample_doc.split()
                vec2 = map(float, vec2_str)
                self.data2[i, :] = np.array(vec2)
                i = i + 1
            np.save(sample_theta_npy, self.data2)

    def jgibblda_inf(self, text):
        cur_time = datetime.now().strftime('%Y%m%d%H%M%S%f')
        inf_file_name = path_define.INF_FILE_NAME_FMT % (cur_time)
        ref_content = []
        ref_content.append('1\n')
        ref_content.append(text)
        ref_file = open(inf_file_name, 'w')
        ref_file.writelines(ref_content)
        ref_file.close()
        subprocess.call(["/bin/bash", "mylda/gen-ref-theta.sh", self.model_str, os.path.abspath(inf_file_name)])
        #lda_command = "java -cp /home/gwlin/dev/JGibbLDA-v.1.0/bin:/home/gwlin/dev/JGibbLDA-v.1.0/lib/args4j-2.0.6.jar " \
        #             "jgibblda.LDA -inf -model " + self.model_str + " -dir " + os.path.dirname(os.path.abspath(inf_file_name)) + " -dfile " + os.path.basename(os.path.abspath(inf_file_name))
        #print lda_command
        #subprocess.call(lda_command)
        inf_theta_filename = inf_file_name + '.' + self.model_str + '.theta'
        inf_theta_file = open(inf_theta_filename, 'r')
        inf_theta = inf_theta_file.readline()
        inf_theta_file.close()
        return  inf_theta

    def calc_score(self, new_doc_theta):
        """
        计算一个 new_doc 的 theta 向量与其他sample_docs 的theta 向量的距离，并排序
        :param new_doc_theta: new document distribution on k topics
        :param sample_docs_theta_path: sample documents theta, model.theta, M * K
        :return:indices of ranking docs
        """
        # 构造data1, 1*K 向量，new_doc_dtb is jgibblda -inf 生成的theta值, one doc distribution of k topics
        vec1 = map(float, new_doc_theta.split())
        print len(vec1)
        data1 = np.array(vec1)
        # 逐个doc比较求欧氏距离
        result = la.norm(data1 - self.data2, axis=1)
        return result

    def search_as_dict(self, query_text, top_n=20):
        query_md5 = utils.get_md5(query_text)
        query_theta_path = path_define.DATA_DIR + query_md5 + ".pkl"
        print query_theta_path
        query_theta = utils.load_or_calc(query_theta_path, self.jgibblda_inf, query_text)
        #query_theta = self.jgibblda_inf(query_text)
        result = self.calc_score(query_theta)
        rst_index = np.argsort(result)
        print rst_index[:10]
        # rst_index 是从大到小的序号，result是文件顺序的欧式距离的值
        i = 0
        rst_dict = {}
        while i < top_n:
            real_index = rst_index[i]
            file_name = self.sample_name_list[real_index]
            rst_dict[file_name] = result[real_index]
            i += 1
        return rst_dict

    def print_topn(self, topn_zip):
        i = 1
        for (name, score) in topn_zip:
            print "%d, (%s, %s)" % (i, name, score)
            i += 1
