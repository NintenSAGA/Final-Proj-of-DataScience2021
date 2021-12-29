import jieba
import re
import time
import jieba.posseg as pseg
import sys
from src import NLP
from collections import OrderedDict

# 全国法院名单.txt
jieba.load_userdict(NLP.__path__[0]+'/jiebaVersion/全国法院名单.txt')

# 罪名.txt
jieba.load_userdict(NLP.__path__[0]+'/jiebaVersion/罪名.txt')

# 其他需要增加权重的词语
jieba.load_userdict(NLP.__path__[0]+'/jiebaVersion/userdict.txt')


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


def get_danger_info(text):
    """
    得到危险驾驶信息

    :parameter text:文本 -> str
    :return danInfo -> str
    """

    lines = text.split('\n')
    danInfo = ''

    mea_a = ['ｍｇ', 'mg', '毫克']
    mea_b = ['ｍｌ', 'ml', '毫升']
    num = '\\d+(\\.\\d+)?'

    p = '{}({})[^{}]+({})?({})'.format(num, '|'.join(mea_a), ''.join(mea_a) + ''.join(mea_b), num, '|'.join(mea_b))

    pattern = re.compile(r'{}'.format(p))

    pos = 0
    match = pattern.search(text, pos)
    while match:
        pos = match.span()[1]
        danInfo = match.group(0)
        match = pattern.search(text, pos)

    return danInfo

    #
    # for i in range(len(lines)):
    #     if re.search(r'\d+(\.\d+)?(ｍｇ|mg|毫克).+\d+(ｍｌ|ml|mL|毫升)', lines[i], re.DOTALL):
    #         danInfo = re.search(r'\d+(\.\d+)?(ｍｇ|mg|毫克).+\d+(ｍｌ|ml|mL|毫升)', lines[i], re.DOTALL).group(0)
    #         break
    #
    # return danInfo


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
    alcohol = get_danger_info(text)
    word_freq = {}

    with open(NLP.__path__[0]+'/jiebaVersion/wF.txt', 'w') as wFfile:
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
    # 个人基本信息
    name = []

    # 地区
    province = []
    city = []

    # 罪名
    accusation = []

    # 审理法院
    court = []

    # 判决结果
    verdict = []

    # 涉案金额
    money = []

    # 酒精含量
    alcohol = []

    with open(wFfilepath, 'r+') as wFfile:
        lines = wFfile.read().split('\n')

        alcohol_line = lines[0]
        alcohol.append(alcohol_line.split('/ac')[0].strip('(\''))
        if alcohol[0] == '':
            alcohol = []

        verdict_line = lines[1]
        verdict.append(verdict_line.split('/re')[0].strip("('"))

        for line in lines[2:]:
            line = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", " ", line)
            line = line.strip().replace('  ', ' ')
            words = line.split(" ")
            if words[-1] == 're':
                for word in words:
                    if re.search('(罚金|人民币).*元', word):
                        money.append(str(re.search('(罚金|人民币).*元', word).group(0)))
            elif words[1] == 'nr':
                name.append(words[0])
            elif words[1] == 'ct':
                court.append(words[0])
            elif words[1] == 'ns':
                if words[0].endswith("省") or words[0].endswith("自治区"):
                    province.append(words[0])
                elif words[0].endswith("市"):
                    city.append(words[0])
            elif words[0].endswith("罪"):
                if words[1] == 'cg':
                    accusation.append(words[0])
                elif len(words[0]) == 3:
                    accusation.append(words[0])

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
    return return_result(NLP.__path__[0]+'/jiebaVersion/wF.txt')


