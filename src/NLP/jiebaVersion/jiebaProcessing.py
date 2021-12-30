import jieba
import re
import pickle
import jieba.posseg as pseg
from src import NLP
from collections import OrderedDict

WORK_DIR = NLP.__path__[0]+'/jiebaVersion/'
DICTS_DIR = WORK_DIR + 'user_dicts/'
CITY_TO_PROV = pickle.load(open(WORK_DIR + 'city_to_prov.pkl', 'rb'))   # type: {str: str}

# 其他需要增加权重的词语
jieba.load_userdict(DICTS_DIR + 'userdict.txt')
# court_list.txt
jieba.load_userdict(DICTS_DIR + 'court_list.txt')
# accusation_list.txt
jieba.load_userdict(DICTS_DIR + 'accusation_list.txt')
# 省份与城市
jieba.load_userdict(DICTS_DIR + 'city_list.txt')
jieba.load_userdict(DICTS_DIR + 'prov_list.txt')


def get_verdict(text: str):
    """
    根据文本格式，获得判决结果

    :parameter text:文本 -> str
    :return Verdict -> list
    """
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('判决'):
            return lines[i + 1]
    return ''


def get_alcohol(text):
    """
    得到危险驾驶信息

    :parameter text:文本 -> str
    :return danInfo -> str
    """
    alcohol = ''

    mea_a = ['ｍｇ', 'mg', '毫克']
    mea_b = ['ｍｌ', 'ml', '毫升']
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


def process_property(filePath):
    # 处理字典词性
    with open(filePath, 'r+') as file:
        text = file.read()
        lineList = text.split('\n')

    with open(filePath, 'w+') as file:
        for line in lineList:
            file.write(''.join(line+'000'+'\n'))

    file.close()


def process_text(text) -> list:
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


def cal_word_frequency(text):
    """
     获得分词后每个词的词性以及词频，并按词性分类，按词频排序，并写入 wF.txt

     :parameter text：待切割的文本
    """
    filtered_list = process_text(text)
    verdict = get_verdict(text)
    alcohol = get_alcohol(text)
    word_freq = {}

    with open(WORK_DIR + 'wF.txt', 'w') as wFfile:
        for line in filtered_list:
            for word in line:
                s = str(word)
                word_freq[s] = word_freq.get(s, 0) + 1
        sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        wFfile.write('(\'' + alcohol + '/ac' + '\')' + '\n')
        wFfile.write('(\''+verdict + '/re' + '\')'+'\n')

        for item in sorted_word_freq:
            wFfile.write(item[0])
            wFfile.write('\n')

    wFfile.close()


def return_result(wFfilepath):
    """
        计算得到结果

        :parameter wFfilepath: 词频文本路径
        :return result -> OrderedDict[str,list[str]]
    """

    name = []               # 个人基本信息
    province = []           # 地区
    city = []
    accusation = []         # 罪名
    court = []              # 审理法院
    verdict = []            # 判决结果
    money = []              # 涉案金额
    alcohol = []            # 酒精含量

    with open(wFfilepath, 'r+') as wFfile:
        lines = wFfile.read().split('\n')

        alcohol_line = lines[0]
        alcohol.append(alcohol_line.split('/ac')[0].strip('(\''))
        if alcohol[0] == '':
            alcohol = []

        verdict_line = lines[1]
        verdict.append(verdict_line.split('/re')[0].strip("('"))

        prov_pat = re.compile('^.*(省|自治区)')
        city_pat = re.compile('^.*(市|县)')

        for line in lines[2:]:
            line = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", " ", line)
            line = line.strip().replace('  ', ' ')
            words = line.split(" ")

            if words[-1] == 're':
                for word in words:
                    if re.search('(罚金|人民币).*元', word):
                        money.append(str(re.search('(罚金|人民币).*元', word).group(0)))
            elif words[-1] == 'nr':
                name.append(words[0])
            elif words[-1] == 'ct':
                court.append(words[0])
                # 提取省份
                prov_match = prov_pat.search(words[0])
                # case 1: 非直辖市
                if prov_match:
                    province.insert(0, prov_match.group(0))
                    city_match = city_pat.search(words[0][prov_match.span()[1]:])
                    if city_match:
                        city.insert(0, city_match.group(0))
                # case 2: 直辖市
                else:
                    city_match = city_pat.search(words[0])
                    if city_match:
                        city_name = city_match.group(0)
                        province.insert(0, city_name)
                        city.insert(0, city_name)
            elif words[-1] == 'prov':
                province.append(words[0])
            elif words[-1] == 'city':
                city.append(words[0])
            elif words[-1] == 'cg':
                accusation.append(words[0])

    # side cases
    # 1. 审理法院占用省份词条
    if len(province) == 0 and len(court) != 0:
        province.append(re.search('.*(省|自治区)', court[0]).group(0))
    # 2. 直辖市
    if len(city) == 0 and len(province) != 0 and province[0].endswith('市'):
        city.append(province[0])

    result = OrderedDict()
    result['姓名'] = name
    result['省份'] = province
    result['城市'] = city
    result['罪名'] = accusation
    result['审理法院'] = court
    result['判决结果'] = verdict
    result['罚金金额'] = money
    result['酒精含量'] = alcohol

    return result


def to_string(s):
    res = ""
    for word in s:
        res += (word + ' ')
    return res


def get_result(text):
    """
        param: text -> 文书所在文件夹路径
        return: result -> OrderedDict[str,list[str]]
    """
    cal_word_frequency(text)
    return return_result(WORK_DIR + 'wF.txt')


