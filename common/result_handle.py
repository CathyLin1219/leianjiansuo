#!/usr/bin/env python
# coding=UTF-8
import re, codecs
import utils, path_define


def save_rst_report(final_rst_pkl, dict_name2json):
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


def save_rst_list(rst, save_path):
    buffer = ''
    i = 1
    for file_name, score in rst:
        buffer += "%d\t%s\t%.3f\n" % (i, file_name, score)
        i += 1
    save_file = open(save_path, 'w')
    save_file.write(buffer)
    save_file.close()


def analyze_luc_vs_lda(luc_dict, lda_dict, final_rank):
    luc_set = set(luc_dict.keys())
    lda_set = set(lda_dict.keys())
    rank_list = list(zip(*final_rank)[0])
    luc_pos_list = group_rank_pos(luc_set, rank_list)
    lda_pos_list = group_rank_pos(lda_set, rank_list)
    print "Lucene pos list in final rank: ", luc_pos_list
    print "\tthe average of Lucene pos", sum(map(float, luc_pos_list))/len(luc_pos_list)
    print "LDA pos list in final rank: ", lda_pos_list
    print "\tthe average of LDA pos", sum(map(float, lda_pos_list))/len(lda_pos_list)


def group_rank_pos(group_a, rank_list):
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


def save_for_human_rating(query_case_name, mechine_rank_rst, top_n):
    """
    先列查询的文书，再列候选的文书，每两个文书之间空两行，一行一段，保存为csv，供资源部同事在excel中查看
    :param query_case_name:
    :param mechine_rank_rst:
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

    # 添加候选的文书
    i = 0
    for file_name, score in mechine_rank_rst:
        lines.append("%s\n" % file_name)
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
