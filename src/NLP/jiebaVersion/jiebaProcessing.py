import jieba
import re
import pickle
import jieba.posseg as pseg
from src import NLP
from collections import OrderedDict

WORK_DIR = NLP.__path__[0] + '/jiebaVersion/'
DICTS_DIR = WORK_DIR + 'user_dicts/'
CITY_TO_PROV = pickle.load(open(WORK_DIR + 'city_to_prov.pkl', 'rb'))  # type: {str, str}
punc = ['。', '，', '；', '？', '！', '：', ',', '.', ';', ':', '?', '!', '（',
        '】']

# 其他需要增加权重的词语
jieba.load_userdict(DICTS_DIR + 'userdict.txt')
# court_list.txt
jieba.load_userdict(DICTS_DIR + 'court_list.txt')
# accusation_list.txt
jieba.load_userdict(DICTS_DIR + 'accusation_list.txt')
# 省份与城市
jieba.load_userdict(DICTS_DIR + 'city_list.txt')
jieba.load_userdict(DICTS_DIR + 'prov_list.txt')


def get_result(text) -> OrderedDict:
    """
        param: text -> 文书文本
        return: result -> OrderedDict[str,list[str]]
    """

    return parse_word_freq(cal_word_freq(text), text)


# ==============================计算词频============================== #
def cal_word_freq(text: str) -> dict:
    """
     获得分词后每个词的词性以及词频，并按词性分类，按词频排序，并返回字典

     :parameter text：待切割的文本
     :return: dict
    """
    filtered_list = text_filter(text)
    alcohol = get_alcohol(text)
    penalty = get_penalty(text)
    money = get_money(text)

    word_dict = {}

    word_freq = {}
    for words in filtered_list:
        for word in words:
            s = str(word)
            word_freq[s] = word_freq.get(s, 0) + 1
    sorted_words = sorted(word_freq.keys(), key=lambda x: word_freq[x], reverse=True)

    word_dict['ac'] = [alcohol]
    word_dict['mn'] = [money]
    word_dict['pe'] = [penalty]

    for item in sorted_words:
        word, prop = item.split('/')
        temp = word_dict.get(prop, list())
        temp.append(word)
        word_dict[prop] = temp

    return word_dict


def text_filter(text) -> list:
    """
    处理文本，过滤标点符号，并返回list

    :parameter text:文本 -> str
    :return filterLines:过滤后的文本 -> list
    """
    filtered_lines = []
    lines = text.split('\n')
    for line in lines:
        line = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", line)
        if line != '':
            filtered_lines.append(list(pseg.cut(line, True)))

    return filtered_lines


# def get_verdict(text: str):
#     """
#     根据文本格式，获得判决结果
#
#     :parameter text:文本 -> str
#     :return Verdict -> list
#     """
#     lines = text.split('\n')
#     for i, line in enumerate(lines):
#         if line.startswith('判决'):
#             return lines[i + 1]
#     return ''


def get_alcohol(text) -> str:
    """
    得到危险驾驶信息

    :parameter text:文本 -> str
    :return danInfo -> str
    """
    alcohol = ''

    mea_a = ['ｍｇ', 'mg', '毫克', 'mG', 'ｍＧ', 'MG', 'Mg', 'ＭＧ', 'Ｍｇ']
    mea_b = ['ｍｌ', 'ml', '毫升', 'mL', 'ｍＬ', 'ML', 'Ml', 'ＭＬ', 'Ｍｌ', 'ｍ1']
    # ｍｌＭＬＭＧｍｇ
    # 162.28ｍｇ／100ｍ1
    num = '\\d+(\\.\\d+)?'

    p = '{}({})[^{}]+({})?({})'.format(num, '|'.join(mea_a), ''.join(mea_a) + ''.join(mea_b), num, '|'.join(mea_b))

    pattern = re.compile(r'{}'.format(p))

    pos = 0
    match = pattern.search(text, pos)
    while match:
        pos = match.span()[1]
        alcohol = match.group(0)
        match = pattern.search(text, pos)

    return alcohol


def get_penalty(text: str) -> str:
    """
    获取主刑：有期徒刑，拘役，管制，无期徒刑，死刑

    :return:
    """
    penalties = ['管制', '拘役', '有期徒刑']
    sub_pat1 = '|'.join(penalties)
    sub_pat2 = ''.join(punc)+'、'+'（'+'('
    pat = re.compile(r'(判[^{}]*({})[^{}]+)'.format(sub_pat2, sub_pat1, sub_pat2))
    match = pat.findall(text)
    if len(match) > 0:
        return match[-1][0]
    pat_list = ['无期徒刑', '死刑']
    sub_pat1 = '|'.join(pat_list)
    pat = re.compile(r'(判[^{}]*({}))'.format(sub_pat2, sub_pat1))
    match = pat.findall(text)
    if len(match) > 0:
        return match[-1][0]
    return ''


def get_money(text: str) -> str:
    """
    提取附加刑，含罚金与没收

    :param text:
    :return:
    """
    actions = ['罚金', '没收']
    sub_pat1 = '|'.join(actions)
    sub_pat2 = ''.join(punc)+'、'+'（'+'('
    pat = re.compile(r'(({})[^{}]+元)'.format(sub_pat1, sub_pat2))
    match = pat.findall(text)
    if len(match) > 0:
        return match[-1][0]
    return ''


# ==============================生成结果============================== #
def parse_word_freq(word_dict: dict, org_text: str) -> OrderedDict:
    """
        计算得到结果
        :param org_text:
        :parameter word_dict: 词频字典
        :return result -> OrderedDict[str,list[str]]
    """

    name = []  # 个人基本信息
    province = []  # 地区
    city = []
    accusation = []  # 罪名
    court = []  # 审理法院
    # verdict = []  # 判决结果
    money = []  # 涉案金额
    alcohol = []  # 酒精含量
    penalty = []  # 刑罚结果

    prov_pat = re.compile('^.*(省|自治区)')
    city_pat = re.compile('^.*(市|县)')

    # ------------------只取唯一可能项------------------------ #
    pairs = [[alcohol, 'ac', 0],    # 1. 酒精
             [money, 'mn', 0],      # 2. 金额
             [penalty, 'pe', 0]]   # 3. 主刑
    for pair in pairs:
        pool, key, i = pair
        temp = word_dict.get(key, [''])
        if temp[i] != '':
            pool.append(temp[i])

    # ------------------单独处理法院------------------------ #
    tmp_court = word_dict.get('ct', [''])[0]
    if tmp_court != '':
        court.append(tmp_court)
        # 提取省份
        prov_match = prov_pat.search(tmp_court)
        # case 1: 非直辖市
        if prov_match:
            province.insert(0, prov_match.group(0))
            city_match = city_pat.search(tmp_court[prov_match.span()[1]:])
            if city_match:
                city.insert(0, city_match.group(0))
        # case 2: 直辖市
        else:
            city_match = city_pat.search(tmp_court)
            if city_match:
                city_name = city_match.group(0)
                province.insert(0, city_name)
                city.insert(0, city_name)

    # ------------------多可能项------------------------ #
    pairs = [[name, 'nr'],
             [province, 'prov'],
             [city, 'city'],
             [accusation, 'cg']]
    for pair in pairs:
        pool, key = pair  # type: list, str
        for i in word_dict.get(key, []):
            pool.append(i)

    # side cases
    # 1. 直辖市
    if len(city) == 0 and len(province) != 0 and province[0].endswith('市'):
        city.append(province[0])
    # 2. 未找到省份信息
    if len(province) == 0 and len(city) != 0:
        province.append(CITY_TO_PROV[city[0]])
    # 3. 法院信息不规范
    if len(court) == 0 and len(province) != 0 and len(city) != 0:
        court.append('{}{}中级人民法院'.format(province[0], city[0]))
    # 4. 罪名补充
    punc_unit = ''.join(punc)
    pat = re.compile(r'(被告人[^{}]+?犯([^{}]+罪))'.format(punc_unit, punc_unit))
    match = pat.findall(org_text)
    for temp in match:
        accusation.append(temp[1])
    # ------------------单独处理罪由------------------------ #
    accu_freq_dict = {}
    for accu in accusation:
        accu_freq_dict[accu] = accu_freq_dict.get(accu, 0) + 1
    accusation = sorted(sorted(accu_freq_dict.keys(), key=lambda x: len(x), reverse=True),
                        key=lambda x: accu_freq_dict.get(x), reverse=True)

    result = OrderedDict()
    result['姓名'] = name
    result['省份'] = province
    result['城市'] = city
    result['审理法院'] = court
    result['罪名'] = accusation
    result['主刑'] = penalty
    result['附加刑'] = money
    result['酒精含量'] = alcohol

    return result

