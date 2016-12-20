#!/usr/bin/env python
# coding=UTF-8
import sys, subprocess, re, os
import utils


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
