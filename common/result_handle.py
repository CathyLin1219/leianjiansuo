#!/usr/bin/env python
# coding=UTF-8
import re, codecs
import utils, path_define, xls_parser, metric


class ResultHandler:
    def __init__(self):
        # 获取测试集数据
        testcase_path = path_define.TESTCASE_DATA
        self.testcase_data = utils.load_or_calc(testcase_path, xls_parser.get_testcase_lables, path_define.TESTCASE_DIR)

    def save_rst_report(self, final_rst_pkl, dict_name2json):
        report_filename = final_rst_pkl + "_report.txt"
        report_file = open(report_filename, 'w')

        final_rst = utils.load_pyobj(final_rst_pkl)
        i = 1
        lines = []
        for file_name, score in final_rst:
            utils.debug_log("format rst top ", i)
            spliter = "\n---------------Top%d: %s, %.3f-------------\n" % (i, file_name, score)
            if file_name in dict_name2json:
                details = "criminal_name:" + dict_name2json[file_name]["criminal_name"].encode('utf8')\
                          + ", sentenced_time:" + str(dict_name2json[file_name]["sentenced_time"])\
                          + ", money: " + str(dict_name2json[file_name]["money"]) + "\n"
                desc = dict_name2json[file_name]["description"]
                lines.append(spliter)
                lines.append(details)
                lines.append(desc.encode('utf8'))
            else:
                warn_tip = "%s not found in dict_name2json\n" % file_name
                lines.extend([spliter, warn_tip])
            i += 1
        report_file.writelines(lines)
        report_file.close()


    def save_rst_list(self, rst, save_path):
        buffer = ''
        i = 1
        for file_name, score in rst:
            buffer += "%d\t%s\t%.3f\n" % (i, file_name, score)
            i += 1
        save_file = open(save_path, 'w')
        save_file.write(buffer)
        save_file.close()

    def analyze_luc_vs_lda(self, luc_dict, lda_dict, final_rank):
        luc_set = set(luc_dict.keys())
        lda_set = set(lda_dict.keys())
        rank_list = list(zip(*final_rank)[0])
        luc_pos_list = self.group_rank_pos(luc_set, rank_list)
        lda_pos_list = self.group_rank_pos(lda_set, rank_list)
        print "Lucene pos list in final rank: ", luc_pos_list
        print "\tthe average of Lucene pos", sum(map(float, luc_pos_list))/len(luc_pos_list)
        print "LDA pos list in final rank: ", lda_pos_list
        print "\tthe average of LDA pos", sum(map(float, lda_pos_list))/len(lda_pos_list)

    def group_rank_pos(self, group_a, rank_list):
        """
        返回 group_a 中的元素在rank_list中的位置列表
        :param group_a: set
        :param rank_list: list
        :return:
        """
        i = 0
        pos_list = []
        while i < len(rank_list):
            if rank_list[i] in group_a:
                pos_list.append(i)
            i += 1
        return pos_list

    def save_for_human_rating(self, query_case_name, machine_rank_rst, top_n):
        """
        先列查询的文书，再列候选的文书，每两个文书之间空两行，一行一段，保存为csv，供资源部同事在excel中查看
        :param query_case_name:
        :param machine_rank_rst:
        :param top_n:
        :return:
        """
        lines = []
        # 手动添加BOM，否则excel打开中文乱码
        lines.append(codecs.BOM_UTF8)
        # 先添加查询的文书
        lines.append("%s\n" % query_case_name)
        f = open(path_define.CRIMINAL_DIR + query_case_name)
        text = f.read()
        f.close()
        text = re.sub('\n+', '\n', text)
        lines.append(text)
        lines.append('\n\n\n')
        # 查看检索文本是否在测试集中
        if query_case_name in self.testcase_data:
            cur_query = self.testcase_data[query_case_name]
        else:
            cur_query = {}
        # 添加候选的文书
        i = 0
        for file_name, score in machine_rank_rst:
            if file_name in cur_query:
                cur_grade = cur_query[file_name]
            else:
                cur_grade = 0
            lines.append("%s,%d\n" % (file_name, cur_grade))
            f = open(path_define.CRIMINAL_DIR + file_name)
            text = f.read()
            f.close()
            text = re.sub('(\r\n)+|\n+', '\n', text)
            lines.append(text)
            lines.append('\n\n\n')
            i += 1
            if i >= top_n:
                break
        # write to file
        save_path = path_define.HUMAN_RATING_PATH_FMT % (query_case_name, top_n)
        save_file = open(save_path, 'w')
        save_file.writelines(lines)
        save_file.close()


    def measure_with_testcase(self, case_name, rst):
        ranking_lst = []
        if case_name not in self.testcase_data:
            print '%s is not in testcases!' % case_name
            return
        cur_testcase = self.testcase_data[case_name]
        for i in range(0, 30):
            file_name = rst[i][0]
            if file_name not in cur_testcase:
                ranking_lst.append(0)
            else:
                ranking_lst.append(cur_testcase[file_name])
        print case_name + 'top 30 ranking:'
        print ranking_lst

