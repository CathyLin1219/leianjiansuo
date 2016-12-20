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
pattern_dict['money'] = ['([0-9lO,，.＋一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]+)(元)']
pattern_dict['weight'] = [u'([0-9lO,，.＋一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]+)(克|毫克|g|mg|kg)']
pattern_dict['alcohol'] = [u'([0-9lO.＋↑]+)(mg|mg|㎎|MG|毫克|Mg)']
pattern_dict['count'] = ['([0-9lO,，.＋一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]+)(次|起)']
pattern_dict['person_count'] = [u'([0-9lO,，.＋一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]+)(人)']
pattern_dict['injure'] = [u'(轻微伤|轻伤|重伤)([0-9lO,，.＋一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]+级)*']
pattern_dict['disability'] = [u'([0-9lO,，.＋一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]+级)*(伤残|残疾)']
pattern_dict['death_count'] = [u'([0-9lO,，.＋一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]+)(人死亡)']
pattern_dict['injure_count'] = [u'([0-9lO,，.＋一二两三四五六七八九十百千仟万多余壹贰叁肆伍陆柒捌玖拾佰萬]+)(人重伤)']


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

com_pattern_dict = {}
# com_pattern_dict[''] = [u'()', u'()', u'()', u'()', ]
com_pattern_dict['crime_name'] = [u'()', u'()', u'()', u'()', ]
com_pattern_dict['recidivism'] = [u'(再犯|累犯|前科|惯犯)']
com_pattern_dict['renzui'] = [u'(坦白)', u'(当庭认罪|自愿认罪)', u'(无异议|不持异议|没有异议)', u'(如实供述)']
com_pattern_dict['compensation'] = [u'(赔偿|和解协议)']
com_pattern_dict['liangjie'] = [u'(谅解)']
com_pattern_dict['teenager'] = [u'(未满14岁)', u'(未满16岁)', u'(未满18岁)', u'(未满十四岁)', u'(未满十六岁)', u'(未满十八岁)', u'(未成年)']
com_pattern_dict['failed'] = [u'(未遂)', u'(中止犯罪)']
com_pattern_dict['zishou'] = [u'(自首)']
com_pattern_dict['ligong'] = [u'(立功)']

com_pattern_list = ['再犯|有前科|惯犯', '累犯', '赔偿|和解协议', '谅解', '未满14岁|未满十四岁',
                    '未满16岁|未满十六岁', '未满18岁|未满十八岁', '75岁以上|75周岁以上|七十五周岁以上',
                    '未遂', '中止犯罪', '立功', '自首|主动投案', '癔症', '聋哑|盲|瞎子', '主犯', '从犯',
                    '坦白', '当庭认罪|自愿认罪|无异议|不持异议|没有异议|供认不讳', '如实供述']

sp_pattern_dict = {}
sp_pattern_dict['theft'] = ['入室|入户|撬锁|翻窗|爬窗户|爬窗|撬门', '扒窃', '医院盗窃', '盗窃救灾款',
                            '退赃|退赔|归还|退回部分赃款|退回全部赃款|退回部分赃款|赃款返还|追回发还|追回并发还|已发还|并发还',
                            '持刀|器械|凶器']
sp_pattern_dict['theft'].extend(pattern_dict['money'])
sp_pattern_dict['theft'].extend(pattern_dict['count'])

sp_pattern_dict['kill'] = ['杀死母亲|杀死父亲|抛尸|手段残忍|杀死儿子|杀死女儿|杀死孩子', '激情杀人|义愤杀人',
                           '防卫过当', '助人自杀']


