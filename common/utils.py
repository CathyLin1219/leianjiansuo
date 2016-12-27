# coding=UTF-8

import pickle, os, json, hashlib
import defines


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
        # 防止除数为0
        if max_value == 0:
            return name_score_dict
        prop_factor = 100.0 / max_value

    for name in name_score_dict:
        if prop:
            name_score_dict[name] = name_score_dict[name] * prop_factor
        else:
            name_score_dict[name] = 1.0 / (1.0 + name_score_dict[name])

    if not prop:
        normalize_score(name_score_dict, True)
    return name_score_dict


def get_md5(txt):
    md5_obj = hashlib.md5()
    md5_obj.update(txt)
    md5_str = md5_obj.hexdigest()
    return md5_str


def debug_log(*args, **kwargs):
    if defines.DEBUG:
        print "=====", args, kwargs



