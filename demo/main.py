#coding=utf8

from full_rank import full_rank
from common import path_define, utils, defines
from mylucene.search_files import lucene_rank
from mylda.search_files import lda_rank
from myelem.search_files import elem_rank
from myother.search_files import similar_class_crime

def main():
    global_inst = full_rank()
    #global_inst.general_rank("criminalname0_351469.txt")  # 案例1
    #global_inst.general_rank("criminalname0_372322.txt")  # 案例2
    #global_inst.general_rank("criminalname0_51504.txt")  # 案例3
    #global_inst.general_rank("criminalname0_1444427.txt")
    #global_inst.general_rank("criminalname9_603652.txt") # 故意杀人
    query_cases_file = open("data/theft_cases_name.txt", 'r') # 盗窃罪
    #query_cases_file = open("data/kill_cases_name.txt", 'r')   # 故意杀人罪
    query_cases = query_cases_file.readlines()
    query_cases_file.close()
    for query_case in query_cases:
        query_case = query_case.strip()
        global_inst.general_rank(query_case)


def test_luc(case_name, case_desc):
    luc_inst = lucene_rank()
    cur_case_luc_cand_path = path_define.CASE_LUC_CAND_PATH_FMT % case_name
    luc_cand = utils.load_or_calc(cur_case_luc_cand_path, luc_inst.search_as_dict, case_desc)


def test_lda(case_name, case_desc):
    lda_inst = lda_rank(path_define.LDA_MODEL_STR)
    cur_case_lda_cand_path = path_define.CASE_LDA_CAND_PATH_FMT % case_name
    lda_cand = utils.load_or_calc(cur_case_lda_cand_path, lda_inst.search_as_dict, case_desc)

def test_elem(case_name):
    inst = elem_rank()
    cand_list = ['criminalname9_1527038.txt', 'criminalname9_1494452.txt', 'criminalname9_1420298.txt', 'criminalname9_1556432.txt']
    inst.search_as_dict(case_name, 8, cand_list)

def test_save_report(pkl_file):
    global_inst = full_rank()
    global_inst.save_rst(pkl_file)

def test_sim_class(crime_index):
    # get random_of_similar_crime, tpye is list
    sim_inst = similar_class_crime()
    sim_cand = sim_inst.random_get_similar_cases(crime_index, 5000)
    print len(sim_cand)

if __name__ == '__main__':
    main()
    #test_sim_class(8)
    #test_elem('criminalname9_38253.txt')
    #desc = "公诉 机关 指控 ： 2015年 7月 2日 9时 21 分 许 ， 被告人 徐 先 水 在 本市 上 城区 大学路 新村 25 幢 水果 店 附近 ， 用 一 只 手 提 编织袋 作 掩护 ， 趁 被害人 顾某 不 备 ， 从 其 挽 在 左手臂 上 的 白色 环保 袋内 窃 得 蓝色 绣花 钱包 一个 （ 内 有 人民币 81.5 元 ， 钥 匙 一 串 ） 之后 被告人 徐先水 在 逃离 现场 过程 中 被 周边 群众 抓获 小营 派出所 民警 接 群众 报警 后 赶到 现场 ， 将 被告人 徐 先 水 传唤 回 所 进行 调查 案 发 后 ， 涉案财物 已 被 追 回 并发 还给 被害人"
    #name = "criminalname0_952752.txt"
    #test_luc(name, desc)
    #test_lda(name, desc)
    #test_save_report("data/criminalname9_603652.txt_gnr_cand_0.4_0.4_0.2.pkl")
