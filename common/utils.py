# coding=UTF-8

import pickle, os, json, hashlib
import defines
import numpy as np

def dump_pyobj(pyobj, filename):
    if filename.strip() != '':
        output = open(filename, 'wb')
        pickle.dump(pyobj, output)
        output.close()


def load_pyobj(filename):
    if filename.strip() != '':
        input = open(filename, 'rb')
        rst = pickle.load(input)
        input.close()
        return rst


def load_or_calc(loadpath, calc_func, *arg):
    if os.path.exists(loadpath):
        return load_pyobj(loadpath)
    else:
        rst = calc_func(*arg)
        dump_pyobj(rst, loadpath)
        return rst


def gen_name2json_dict(json_file_path):
    json_file = open(json_file_path, 'r')
    json_lines = json_file.readlines()
    json_file.close()

    dict_name2json = {}
    for json_line in json_lines:
        json_obj = json.loads(json_line)
        file_name = json_obj["file_name"]
        # print  i, file_name
        dict_name2json[file_name] = json_obj
    return dict_name2json


def normalize_score(name_score_dict, prop=True):
    """
    归一化，最好的为100
    :param name_score_dict: 文件名与的分的词典
    :param prop: true 正比， false 反比
    :return: 归一化后的得分字典
    """
    if prop:
        max_value = max(name_score_dict.values())
        min_value = min(name_score_dict.values())

        for name in name_score_dict:
            if (max_value - min_value) == 0:
                name_score_dict[name] = 1
            else:
                name_score_dict[name] = (name_score_dict[name] - min_value) / (max_value - min_value)
    else:
        for name in name_score_dict:
            name_score_dict[name] = 1.0 / (1.0 + name_score_dict[name])
        normalize_score(name_score_dict, True)
    return name_score_dict

def max_min_normalization(arr, prop=True):
    '''
    (0,1) 标准化
    :param arr: 一维 numpy array
    :param prop:true 正比， false 反比
    :return:
    '''
    arr = np.asfarray(arr)
    if prop:
        max_val = np.max(arr)
        min_val = np.min(arr)
        arr = (arr - min_val) / (max_val - min_val)
        return arr
    else:
        arr = 1.0 / (1.0 + arr)
        return max_min_normalization(arr, True)

def get_md5(txt):
    md5_obj = hashlib.md5()
    md5_obj.update(txt)
    md5_str = md5_obj.hexdigest()
    return md5_str


def debug_log(*args, **kwargs):
    if defines.DEBUG:
        print "=====", args, kwargs


num_dict = {u'零': 0, u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7, u'八': 8, u'九': 9, u'十': 10, u'百': 100,
        u'千': 1000, u'万': 10000,
        u'０': 0, u'１': 1, u'２': 2, u'３': 3, u'４': 4, u'５': 5, u'６': 6, u'７': 7, u'８': 8, u'９': 9,
        u'壹': 1, u'贰': 2, u'叁': 3, u'肆': 4, u'伍': 5, u'陆': 6, u'柒': 7, u'捌': 8, u'玖': 9, u'拾': 10, u'佰': 100,
        u'仟': 1000, u'萬': 10000,
        u'亿': 100000000,
        u'0': 0, u'1': 1, u'2': 2, u'3': 3, u'4': 4, u'5': 5, u'6': 6, u'7': 7, u'8': 8, u'9': 9, u'两': 2}


def chn2int(a, encoding="utf-8"):
    if isinstance(a, str):
        a = a.decode(encoding)

    count = 0
    result = 0
    tmp = 0
    Billion = 0

    if a == u'万':
        return 10000
    elif a == u'千':
        return 1000
    elif a == u'百':
        return 100
    elif a == u'十':
        return 10

    while count < len(a):
        tmpChr = a[count]
        # print tmpChr
        tmpNum = num_dict.get(tmpChr, None)
        # 如果等于1亿
        if tmpNum == 100000000:
            result = result + tmp
            result = result * tmpNum
            # 获得亿以上的数量，将其保存在中间变量Billion中并清空result
            Billion = Billion * 100000000 + result
            result = 0
            tmp = 0
        # 如果等于1万
        elif tmpNum == 10000:
            result = result + tmp
            result = result * tmpNum
            tmp = 0
        # 如果等于十或者百，千
        elif tmpNum >= 10:
            if tmp == 0:
                tmp = 1
            result = result + tmpNum * tmp
            tmp = 0
        # 如果是个位数
        elif tmpNum is not None:
            tmp = tmp * 10 + tmpNum
        count += 1
    result = result + tmp
    result = result + Billion
    return result
