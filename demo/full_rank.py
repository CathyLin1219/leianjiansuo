# coding=UTF-8

import pickle, os, sys
from common import path_define, utils, defines, result_handle
from mylucene.search_files import lucene_rank
from mylda.search_files import lda_rank
from myelem.search_files import elem_rank
from myjudgrst.search_files import judge_rank
import numpy as np

class full_rank:
    def __init__(self):
        name2json_dict_pkl = path_define.MAP_NAME2JSON + '.pkl'
        self.dict_name2json = utils.load_or_calc(name2json_dict_pkl, utils.gen_name2json_dict,\
                                                 path_define.MAP_NAME2JSON)
        self.luc_inst = lucene_rank()
        self.lda_inst = lda_rank(path_define.LDA_MODEL_STR)
        self.elem_inst = elem_rank()
        self.judg_inst = judge_rank(self.dict_name2json)


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
        # 案例1
        """case_desc = "公诉 机关 指控 ： 2015年 7月 2日 9时 21 分 许 ， 被告人 徐 先 水 在 本市 上 \
        城区 大学路 新村 25 幢 水果 店 附近 ， 用 一 只 手 提 编织袋 作 掩护 ， 趁 被害人 顾某 不 备 ， \
        从 其 挽 在 左手臂 上 的 白色 环保 袋内 窃 得 蓝色 绣花 钱包 一个 （ 内 有 人民币 81.5 元 ，\
         钥 匙 一 串 ） 之后 被告人 徐先水 在 逃离 现场 过程 中 被 周边 群众 抓获 小营 派出所 民警 接 \
         群众 报警 后 赶到 现场 ， 将 被告人 徐 先 水 传唤 回 所 进行 调查 案 发 后 ， \
         涉案财物 已 被 追 回 并发 还给 被害人"
        """
        # 案例2 criminalname0_372322.txt
        #case_desc = "2015年 1月 13日 19时 许 ， 被告人 陈某 驾驶 二 轮 摩托车 到 永安市 佳洁 购物 广场 肯德基店 前 载客 时 ， 发现 被害人 林某 乙停 于 该处 的 闽 J ××××× 轿车 车门 未 锁 好 即 离开 ， 遂 乘 周边 无 人 之 机 ， 上前 打开 车门 盗 走 D & G 牌 男士 手提包 一个 ， 包 内 有 现金 人民币 800 余 元 、 LACOSTE 牌 男士 手 抓 包 一个 、 Seagate 牌 移动 硬盘 一个 之后 ， 被告人 陈某 驾驶 摩托车 回到 永安市 燕南 荣兴路 52 号 家中 ， 将 手提包 中 800 余 元 现金 取出 后 ， 将 手提包 及 包 内 其他 品 藏匿 于 一 楼 走廊 的 杂物堆 里 经 永安市 价格 认证 中心 鉴定 ， 被盗 的 D & G 牌 男士 手提包 价值 人民币 8400 元 ， LACOSTE 牌 男士 手 抓 包 价值 人民币 150 元 ， Seagate 牌 移动 硬盘 价值 人民币 270 元 被告人 陈某 于 2015年 1月 15日 被 永安市 公安局 抓获 归案"
        # 案例3 criminalname0_51504.txt
        #case_desc = "2015年 1月 16日 5时 许 ， 被告人 孙友江 在 余姚市 泗门镇 振华路 6 号 迪波 电器 有限公司 1 楼 车间 上班 时 ， 乘 虚窃 得 被害人 张亲艳 放在 羽绒服 口袋 内 的 现金 人民币 3600 元 2015年 1月 19日 ， 被告人 孙友江 被 余姚市 公安局 民警 抓获 案 发 后 ， 赃款 已 追 回"
        # criminalname0_1444427.txt
        #case_desc = "2015年 9月 13日 凌晨 ， 被告人 李某 采用 撬门 的 方式 潜入 本区 双屿 街道 屿头 后 江北路 34 号 被害人 贺某 经营 的 超市 ， 窃 得 收银台 内 的 现金 人民币 2000 余 元 同年 9月 17日 凌晨 ， 被告人 李某 采用 相同 方式 潜入 双屿 街道 屿头 后江路 42 号 被害人 夏某 经营 的 兴隆 超市 ， 窃 得 柜台 上 的 软壳 中华 香烟 10 条 （ 价值 人民币 5830 元 ） 及 收银台 内 的 人民币 1500 余 元 同年 9月 19日 凌晨 ， 被告人 李某 采用 相同 方式 潜入 双屿 街道 屿头 大 马路 一 弄 2 号 被害人 郭某甲 经营 的 联丰 超市 ， 窃 得 柜台 内 的 硬壳 中华 香烟 5 条 、 芙蓉 王香烟 2 条 、 白沙 香烟 2 条 、 楚风 红金龙 香烟 1 条 （ 共计 价值 人民币 2771 元 ） 及 收银台处 的 人民币 3000 余 元 同年 9月 20日 凌晨 ， 公安人员 在 双屿 街道 上 伊 南山路 54 号 旅馆 202室 抓获 被告人 李某 ， 并 从 其 房间 内 查获 软壳 中华 香烟 9.5 条 、 硬壳 中华 香烟 5 条 、 芙蓉 王香烟 2 条 、 白沙 香烟 2 条 、 楚风 香烟 1 条 及 人民币 4213.5 元 案 发 后 ， 公安人员 已 将 人民币 842.6 元 发 还 被害人 贺某"
        #crime_index = 0


        # criminalname9_603652.txt 故意杀人
        #case_desc = "2014年 春天 ， 被告人 周风月 酒后 以 捉奸 为由 爬梯子 翻墙 进入 侄子 周某 甲 家中 ， 为此 ， 周某 甲 妻子 杨某甲 召集 当家户族 和 娘家 人 杨某乙 等 人 教训 了 周风月 ， 之后 两 家 再 无 来往 2015年 1月 8日 晚 10时 许 ， 周风月 返回 家中拿 了 一 把 单刃 尖刀 到 周某 甲家街 门口 ， 用 刀 将 杨某 乙 小车 的 四 个 轮胎 戳 破  周某甲 和 出来 后 责骂 周风月 ， 并 冲 到 跟前 在 其 左 腮部 捣 了 一 拳 ， 周风 月 将 周某甲 和 左肩部 捅 了 一 刀 ， 周某甲 和 随即 打电话 报警 杨某甲 出门 后 也 责骂 周风 月 不 该 扎胎 ， 周风月 冲 到 杨某 甲 跟前 ， 左手 抱 住 杨某 甲右 肩膀 ， 右手 持 刀 在 其 左 肋部 、 左 胳膊 、 左肩部 、 左胸部 等 部位 连 捅 七 刀 随后 周某甲 、 周某丁 将 周风月 按 倒 在 地 ， 把 匕首 从 其 手中 抢走 ， 王 某某 、 周某甲 、 周某乙 、 杨某甲 围住 殴打 周风月 之后 杨某 甲 、 周某甲 和 被 送 往 民乐县 人民 医院 抢救 周风月 则 返回 家中 又 提 着 菜刀 到 周某 甲家街 门口 ， 因 街门 已 被 周某 戊朝 里 锁 住 ， 周风月 踢 了 一阵 就 将 杨某 乙 轿车 前后 挡风 玻璃 用 菜刀 打碎 ， 随后 用 菜刀 在 自己 脖子 抹 了 两 刀 企图 自杀 ， 但 被 赶到 现场 的 民警 当场 抓获 ， 并 送 民乐县 人民 医院 抢救 经 法医 鉴定 ， 被害人 杨某甲 的 损伤 程度 属 重伤 二级 ， 被害人 周某 甲和 的 损伤 程度 属 轻微伤 ， 被告人 周风月 颈部 的 损伤 程度 属 轻伤 二级 认定"
        #crime_index = 8

        # get lucene result
        top_n = 1000
        cur_case_luc_cand_path = path_define.CASE_LUC_CAND_PATH_FMT % (case_name, top_n)
        luc_cand = utils.load_or_calc(cur_case_luc_cand_path, self.luc_inst.search_as_dict, case_desc, top_n)
        if case_name in luc_cand:
            luc_cand.pop(case_name)
        utils.normalize_score(luc_cand, True)
        utils.debug_log("lucene search done!")
        utils.debug_log("lucene cand: ", luc_cand)

        # get lda result
        top_n = 1000
        cur_case_lda_cand_path = path_define.CASE_LDA_CAND_PATH_FMT % (case_name, top_n)
        lda_cand = utils.load_or_calc(cur_case_lda_cand_path, self.lda_inst.search_as_dict, case_desc, top_n)
        if case_name in lda_cand:
            lda_cand.pop(case_name)
        utils.normalize_score(lda_cand, False)
        utils.debug_log("lda search done!")
        utils.debug_log("lda cand: ", lda_cand)

        # union of lucene + lda
        uni_list = list(set(luc_cand.keys()).union(set(lda_cand.keys())))
        utils.debug_log("lucene + lda union size = ", len(uni_list))

        # calc element result
        cur_case_elem_cand_path = path_define.CASE_ELEM_CAND_PATH_FMT % (case_name, len(uni_list))
        elem_cand = utils.load_or_calc(cur_case_elem_cand_path, self.elem_inst.search_as_dict,
                                       case_name, crime_index, uni_list)
        utils.normalize_score(elem_cand, True)

        # calc judge result similarity
        cur_case_judg_cand_path = path_define.CASE_JUDG_CAND_PATH_FMT % (case_name, len(uni_list))
        judg_cand = utils.load_or_calc(cur_case_judg_cand_path, self.judg_inst.search_as_dict,
                                       case_name, uni_list)

        # 加权求和
        feature_weight = [0.1, 0.1, 0.4, 0.4]
        score_sum_list = self.weighted_sum(luc_cand, lda_cand, elem_cand, judg_cand,
                                           full_name_list=uni_list, weights_list=feature_weight)
        rank_pairs = self.sort_score(uni_list, score_sum_list)


        # # 附加操作
        # 1.统计来源
        result_handle.analyze_luc_vs_lda(luc_cand, lda_cand, rank_pairs)
        # 2.生成人工评级的文本
        result_handle.save_for_human_rating(case_name, rank_pairs, 30)

        # 保存结果，文件名及得分
        general_result_path = path_define.CASE_GENERAL_CAND_PATH_FMT % (case_name, len(uni_list),
                                                                        '_'.join(map(str, feature_weight)))
        utils.dump_pyobj(rank_pairs, general_result_path)
        save_final_path = path_define.CASE_GENERAL_CAND_LIST_PATH_FMT % (case_name, len(uni_list),
                                                                         '_'.join(map(str, feature_weight)))
        result_handle.save_rst_list(rank_pairs, save_final_path)
        # self.save_rst(general_result_path)
        print rank_pairs[:10]


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
        score_matrix = np.empty((cand_len, cand_cnt), np.float)
        utils.debug_log("score_matrix shape is ", score_matrix.shape)
        # 因为可能存在有的排序方法对应的文档不在top，则以该方面的最低分计算
        j = 0
        while j < cand_cnt:
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
        result_handle.save_rst_report(rst_pkl, self.dict_name2json)
