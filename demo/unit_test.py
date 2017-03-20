#coding=utf8
from myelem import patterns
import re
from common import utils


def test_pattern(str):
    patt = re.compile(str)
    se = patt.findall(u'金华市人民检察院起诉指控：2014年1月21日下午（农历2013年12月21日），被告人舒某因感情问题与被害人刘某在浦江县黄宅镇钟村的租住房内发生争执，并产生了杀死刘某的念头。后被告人舒某将刘某推倒在租房内的床上，骑在刘某的肚子上，采用手掐脖子的方法将刘某掐死。接着，被告人舒某又用编织袋将刘某的尸体包裹后藏于租房内的床底下。经法医学检验鉴定：被害人刘某系因被他人外力作用于颈部致机械性窒息而死亡。')
    if se:
        print 'xxxx'
        print se
        print ','.join(se)
        print utils.chn2int(se[0]) + 1
        #for tup in se:
        #    print ','.join(tup)
        #    print utils.chn2int(tup[1]) + 1
    else:
        print 'nothing matched'

if __name__ == '__main__':
    #test_pattern(u'([0-9lO,，一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]*)人?死亡|杀死([0-9lO,，一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]*)人')
    #test_pattern(u'(杀死([0-9lO,，一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]*)人?)|(([0-9lO,，一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]*)人?死亡)')
    #test_pattern(u'(?:杀死(?:[0-9lO,，一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]*)人)|(?:([0-9lO,，一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]*)人死亡)')
    #test_pattern(u'杀死([0-9lO,，一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]*)人')
    test_pattern(u'([0-9lO,，一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]*)人?死亡')
    test_pattern(u'([0-9lO,，一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]*)人?(重伤|轻伤)')