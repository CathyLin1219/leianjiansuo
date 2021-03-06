# coding=UTF-8
#crime_list = ['theft', 'fraud', 'drug', 'driving', 'robbery', 'injure', 'traffic', 'keepdrug', 'kill', 'trouble']

crime_dict = {'theft':('money', 'count', 'means', 'return_money'),\
    'fraud':('money', 'count', 'return_money'),\
    'drug':('weight', 'drug_name', 'count'),\
    'driving':('alcohol', 'driving_sp', 'responsibility', 'death'),\
    'robbery':('count', 'money', 'shoushang', 'robbery_sp', 'death', 'return_money'),\
    'injure':('injure', 'disability', 'injure_count', 'injure_sp'),\
    'traffic':('death_count', 'injure_count', 'escape', 'responsibility'),\
    'keepdrug':('person_count', 'count', 'keepdrug_sp'),\
    'kill':('motivation','kill_sp'),\
    'trouble':('count', 'injure_count', 'injure'),\
    }

pattern_dict={}
pattern_dict['money'] = [u'([0-9lO,，.＋一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]+)元']
pattern_dict['weight'] = [u'([0-9lO,，.＋一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]+)(克|毫克|g|mg|kg)']
pattern_dict['alcohol'] = [u'([0-9lO.＋↑]+)(mg|mg|㎎|MG|毫克|Mg)']
pattern_dict['count'] = [u'([0-9lO,，.＋一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]+)[次起]']
pattern_dict['person_count'] = [u'([0-9lO,，.＋一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]+)(人)']
pattern_dict['injure'] = [u'(轻微伤|轻伤|重伤)([0-9lO,，.＋一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]+级)*']
pattern_dict['disability'] = [u'([0-9lO,，.＋一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]+级)*(伤残|残疾)']
pattern_dict['death_count'] = [u'([0-9lO,，一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]*)人?死亡']
pattern_dict['injure_count'] = [u'([0-9lO,，一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]*)人?(重伤|轻伤)']


# 其他类别,和数字区别在于最外层需要一个括号
pattern_dict['shoushang'] = [u'(轻微伤|轻伤|重伤)']
pattern_dict['death'] = [u'(死亡|撞死|杀死|砍死|致死)']
pattern_dict['means'] = [u'(入室)', u'(入户)', u'(扒窃)']
pattern_dict['drug_name'] = [u'(鸦片)', u'(海洛因)', u'(甲基苯丙胺)', u'(冰毒)', u'(吗啡)', u'(大麻)', u'(可卡因)']
pattern_dict['motivation'] = [u'(激情杀人|义愤杀人)']
pattern_dict['kill_sp'] = [u'(杀死母亲|杀死父亲|抛尸|手段残忍)']
pattern_dict['escape'] = [u'(逃逸)']
pattern_dict['responsibility'] = [u'(同等责任)',u'(全部责任)',u'(主要责任)']
pattern_dict['drug_sp'] = [u'(教唆)', u'(数量引诱)', ]
pattern_dict['driving_sp'] = [u'(无证|无驾驶资格)', u'(无照|无牌照|没有牌照)', u'受伤|重伤|轻伤', u'车受损|车辆受损']
pattern_dict['return_money'] = [u'(退赃|退赔|归还)']
pattern_dict['robbery_sp'] = [u'入户|入室|公共交通|银行|金融机构|冒充军警|持枪|救灾|救济']
pattern_dict['injure_sp'] = [u'器官|雇佣他人|积极抢救']
pattern_dict['keepdrug_sp'] = [u'严重后果|牟利']

com_pattern_list = ['再犯|有前科|惯犯', '累犯', '赔偿|和解协议', '谅解', '未满14岁|未满十四岁',
                    '未满16岁|未满十六岁', '未满18岁|未满十八岁', '75岁以上|75周岁以上|七十五周岁以上',
                    '未遂', '中止犯罪', '立功', '自首|主动投案', '癔症', '聋哑|盲|瞎子', '主犯', '从犯',
                    '坦白', '当庭认罪|自愿认罪|无异议|不持异议|没有异议|供认不讳', '如实供述']

com_pattern_dict = {u'再犯|有前科|惯犯': 4,
                    u'累犯': 4,
                    u'赔偿|和解协议': 5,
                    u'谅解': 5,  # 1.抢劫罪：在这个罪名里相比较其他要素，谅解的稍微弱。2.危险驾驶：这里谅解对判刑结果影响较小
                    u'未满14岁|未满十四岁': 5,
                    u'未满16岁|未满十六岁': 5,
                    u'未满18岁|未满十八岁': 5,
                    u'75岁以上|75周岁以上|七十五周岁以上': 5,
                    u'未遂': 30,
                    u'中止犯罪': 6,
                    u'立功': 6,
                    u'自首|主动投案': 6,
                    u'限定刑事责任能力|限制刑事责任能力': 6,
                    u'聋哑|盲|瞎子': 6,
                    u'主犯': 4,
                    u'从犯': 4,
                    u'坦白|当庭认罪|自愿认罪|无异议|不持异议|没有异议|供认不讳': 2,
                    u'如实供述': 2}

crime_pattern_dict = {}
crime_num_pattern_dict = {}
crime_pattern_dict['theft'] = {u'入室|入户|撬锁|翻窗|爬窗户|爬窗|撬门': 5,
                            u'扒窃': 5,
                            u'医院盗窃': 5,
                            u'盗窃救灾款': 5,
                            u'退赃|退赔|归还|退回部分赃款|退回全部赃款|退回部分赃款|赃款返还|追回发还|追回并发还|已发还|并发还': 5,
                            u'持刀|器械|凶器': 5,
                            u'多次.{0,10}盗窃|多次.{0,10}窃取': 5}


crime_num_pattern_dict['theft'] = {'money': 30,
                                   }


crime_pattern_dict['kill'] = {u'杀死母亲|杀死父亲|抛尸|手段残忍|杀死儿子|杀死女儿|杀死孩子': 3,
                           u'激情杀人|义愤杀人': 5,
                           u'防卫过当': 5,
                           u'助人自杀': 5}

crime_num_pattern_dict['kill'] = {'death_count': 30,
                               'injure_count': 30}


sp_pattern_dict = {}
sp_pattern_dict['theft'] = [u'入室|入户|撬锁|翻窗|爬窗户|爬窗|撬门', u'扒窃', u'医院盗窃', u'盗窃救灾款',
                            u'退赃|退赔|归还|退回部分赃款|退回全部赃款|退回部分赃款|赃款返还|追回发还|追回并发还|已发还|并发还',
                            u'持刀|器械|凶器']
sp_pattern_dict['theft'].extend(pattern_dict['money'])
sp_pattern_dict['theft'].extend(pattern_dict['count'])

sp_pattern_dict['kill'] = [u'杀死母亲|杀死父亲|抛尸|手段残忍|杀死儿子|杀死女儿|杀死孩子', u'激情杀人|义愤杀人',
                           u'防卫过当', u'助人自杀']

sp_pattern_dict['fraud'] = [u'退赃|退赔|归还|退回部分赃款|退回全部赃款|退回部分赃款|赃款返还|追回发还|追回并发还|已发还|并发还',]
sp_pattern_dict['fraud'].extend(pattern_dict['money'])
sp_pattern_dict['fraud'].extend(pattern_dict['count'])

sp_pattern_dict['drug'] = [u'鸦片', u'海洛因', u'甲基苯丙胺|冰毒', u'吗啡|大麻|可卡因|毒品']
sp_pattern_dict['drug'].extend(pattern_dict['weight'])
sp_pattern_dict['drug'].extend(pattern_dict['count'])

sp_pattern_dict['driving'] = [u'醉酒|酒精含量', u'无证|无驾驶资格', u'无照|无牌照|没有牌照',
                              u'轻微伤', u'轻伤', u'重伤', u'车受损|车辆受损', u'超载', u'超速',
                              u'追逐|竞驶', u'全部责任', u'主要责任', u'次要责任', u'运输危险']

sp_pattern_dict['robbery'] = [u'轻微伤', u'轻伤', u'重伤',u'死亡', u'持刀|器械|凶器', u'持枪',
                              u'入室|入户|撬锁|翻窗|爬窗户|爬窗|撬门', '公共交通|公交车',u'银行',
                              u'金融机构', u'冒充军警', u'救灾|赈灾', u'军用物资',
                              u'退赃|退赔|归还|退回部分赃款|退回全部赃款|退回部分赃款|赃款返还|追回发还|追回并发还|已发还|并发还',]
sp_pattern_dict['robbery'].extend(pattern_dict['count'])
sp_pattern_dict['robbery'].extend(pattern_dict['money'])
sp_pattern_dict['robbery'].extend(pattern_dict['person_count'])

sp_pattern_dict['injure'] = [u'轻微伤', u'轻伤', u'重伤',u'导致伤残|导致残疾', u'器官', u'雇佣他人',
                             u'积极抢救',u'凶器|持刀', u'防卫过当', u'残忍', u'被害人有过错']
sp_pattern_dict['traffic'] = [u'重伤',u'死亡', u'逃逸', u'逃逸致死', u'全部责任', u'主要责任', u'次要责任',]
sp_pattern_dict['traffic'].extend(pattern_dict['person_count'])

sp_pattern_dict['keepdrug'] = [u'严重后果', u'牟利', u'容留未成年']
sp_pattern_dict['keepdrug'].extend(pattern_dict['person_count'])
sp_pattern_dict['keepdrug'].extend(pattern_dict['count'])

sp_pattern_dict['trouble'] = [u'轻微伤', u'轻伤', u'重伤',]
sp_pattern_dict['trouble'].extend(pattern_dict['money'])
sp_pattern_dict['trouble'].extend(pattern_dict['person_count'])