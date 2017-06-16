# coding=UTF-8


def statistic_elem_rst(elem_cand, elem_cand_0526):
    total = 0
    diff_cnt = 0
    for key in elem_cand:
        if key in elem_cand_0526:
            total += 1
            if elem_cand[key] != elem_cand_0526[key]:
                diff_cnt += 1
    print 'difference of old and new element ', diff_cnt, '/', total
