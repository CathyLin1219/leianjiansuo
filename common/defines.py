# coding=UTF-8
DEBUG = False
FLAG_LDA = False
FLAG_ELEM = True
FLAG_JUDG = False
LUCENE_RATE = 0.5
LDA_RATE = 0.0
ELEM_RATE = 0.5
JUDG_RATE = 0.0


crime_list = ['theft', 'fraud', 'drug', 'driving', 'robbery', 'injure', 'traffic', 'keepdrug', 'kill', 'trouble']


def enum_crime_name(name):
    if name == u'盗窃':
        return 0
    elif name == u'诈骗':
        return 1
    elif name == u'走私、贩卖、运输、制造毒品':
        return 2
    elif name == u'危险驾驶':
        return 3
    elif name == u'抢劫':
        return 4
    elif name == u'故意伤害':
        return 5
    elif name == u'交通肇事':
        return 6
    elif name == u'容留他人吸毒':
        return 7
    elif name == u'故意杀人':
        return 8
    elif name == u'寻衅滋事':
        return 9


confused_crime = {0: [1],
                  1: [0],
                  2: [],
                  3: [6, 8],
                  4: [9],
                  5: [8, 9],
                  6: [3],
                  7: [],
                  8: [5],
                  9: [4, 5]}
