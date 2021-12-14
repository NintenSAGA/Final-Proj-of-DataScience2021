import jieba
import re
import time
import jieba.posseg as pseg
import sys
from NLP.get_filename import get_all

# 全国法院名单.txt
jieba.load_userdict('/Users/lijiajun/Final-Proj-of-DataScience2021/src/NLP/jiebaVersion/全国法院名单.txt')

# 罪名.txt
jieba.load_userdict('/Users/lijiajun/Final-Proj-of-DataScience2021/src/NLP/jiebaVersion/罪名.txt')

# 其他需要增加权重的词语
jieba.load_userdict('/Users/lijiajun/Final-Proj-of-DataScience2021/src/NLP/jiebaVersion/userdict.txt')


def get_verdict(filepath):
    """ 根据文本格式，获得判决结果

        :parameter filepath:文档路径
        :return Verdict
    """
    with open(filepath, 'r') as file:
        lines = file.read().split('\n')
        for i in range(len(lines)):
            if ("判决如下" or "判决结果" or "判决主文") in lines[i]:
                return lines[i+1]

    return 'None'


def get_danger_info(filepath):
    """
        得到危险驾驶信息

        :parameter filepath:文本路径
        :return danInfo
    """
    with open(filepath, 'r') as file:
        lines = file.read().split('\n')
        danInfo = 'None'
        for i in range(len(lines)):
            if re.search(r'\d+(\.\d+)?(ｍｇ|mg)([／/])\d+(ｍｌ|ml)', lines[i], re.DOTALL):
                danInfo = re.search(r'\d+(\.\d+)?(ｍｇ|mg)([／/])\d+(ｍｌ|ml)', lines[i], re.DOTALL).group(0)
                break

    return danInfo


def process_property(filePath):
    # 处理字典词性
    with open(filePath, 'r+') as file:
        text = file.read()
        lineList = text.split('\n')

    with open(filePath, 'w+') as file:
        for line in lineList:
            file.write(''.join(line+'000'+'\n'))

    file.close()


def process_text(filepath):
    """ 处理文本，过滤标点符号，并返回list

        :parameter filepath:文档路径
        :return filterLines:过滤后的文本
    """
    filterLines = []
    with open(filepath, 'r') as file:
        for line in file:
            line = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", line)
            if line != '':
                filterLines.append(list(pseg.cut(line, True)))

    file.close()
    return filterLines


def cal_word_frequency(filepath):
    """
        获得分词后每个词的词性以及词频，并按词性分类，按词频排序，并写入 wF.txt

        :parameter tex(list)：待切割的文本
    """
    text = process_text(filepath)
    verdict = get_verdict(filepath)
    danInfo = get_danger_info(filepath)
    wordFrequency = {}
    with open('/Users/lijiajun/Final-Proj-of-DataScience2021/src/NLP/jiebaVersion/wF.txt', 'w') as wFfile:
        for line in text:
            for word in line:
                if wordFrequency.get(str(word)):
                    wordFrequency[str(word)] += 1
                else:
                    wordFrequency[str(word)] = 1

        sortedwordFrequency = sorted(wordFrequency.items(), key=lambda x: x[1], reverse=True)
        wFfile.write('(\'' + danInfo + '/ac' + '\')' + '\n')
        wFfile.write('(\''+verdict + '/re' + '\')'+'\n')
        for word in sortedwordFrequency:
            wFfile.write(str(word) + '\n')
    wFfile.close()


def write_result(wFfilepath, num):
    """
        计算得到结果

        :param wFfilepath: 词频文本路径
        :return: 得到文本分析结果
    """
    # 个人基本信息
    personInfo = ["姓名："]

    # 地区
    province = ["省份："]
    city = ["城市："]

    # 罪名
    case_cause = ["罪名："]

    # 审理法院
    court = ["法院："]

    # 判决结果
    sentences = ["判决结果："]

    # 涉案金额
    money = ["判处罚金："]

    # 危险驾驶相关信息
    dan_message = ["酒精含量："]

    with open(wFfilepath, 'r+') as wFfile:
        firstLine = wFfile.readline()
        dan_message.append(firstLine.split('/ac')[0].strip('(\''))
        for line in wFfile:
            line = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", " ", line)
            line = line.strip().replace('  ', ' ')
            words = line.split(" ")
            if words[len(words)-1] == 're':
                for word in words:
                    if word != 're':
                        sentences.append('\n\t' + word)
                    if re.search('(罚金|人民币).*元', word):
                        money.append(str(re.search('(罚金|人民币).*元', word).group(0)))
                        sentences.append('\n\t' + word)
            elif words[1] == 'nr':
                personInfo.append(words[0])
            elif words[1] == 'ct':
                court.append(words[0])
            elif words[1] == 'ns':
                if words[0].endswith("省") or words[0].endswith("自治区"):
                    province.append(words[0])
                elif words[0].endswith("市"):
                    city.append(words[0])
            elif words[0].endswith("罪"):
                if words[1] == 'cg':
                    case_cause.append(words[0])
                elif len(words[0]) == 3:
                    case_cause.append(words[0])


    new_file_name = '/Users/lijiajun/Final-Proj-of-DataScience2021/src/NLP/jiebaVersion/~result/'+str(num)+'标注.txt'
    resultfile = open(new_file_name, 'w')
    resultfile.write(to_string(personInfo) + '\n')
    resultfile.write(to_string(province) + '\n')
    resultfile.write(to_string(city) + '\n')
    resultfile.write(to_string(case_cause) + '\n')
    resultfile.write(to_string(court) + '\n')
    resultfile.write(to_string(sentences) + '\n')
    resultfile.write(to_string(money) + '\n')
    resultfile.write(to_string(dan_message) + '\n')


def to_string(s):
    res = ""
    for word in s:
        res += (word + ' ')
    return res


def process_bar(num, total):
    rate = float(num)/total
    ratenum = int(100*rate)
    r = '\r[{}{}]{}%'.format('*'*ratenum,' '*(100-ratenum), ratenum)
    sys.stdout.write(r)
    sys.stdout.flush()


def get_result(source_text_path, num):
    """
        param: source_text_path:文书所在文件夹路径
    """
    print("Log:获取文书路径")
    time.sleep(1)
    filepaths = get_all(source_text_path)
    print("Log:已获取")
    time.sleep(1)
    i = 0
    print("Log:开始处理")
    for j in range(min(num, len(filepaths))):
        cal_word_frequency(filepaths[j])
        write_result('/Users/lijiajun/Final-Proj-of-DataScience2021/src/NLP/jiebaVersion/wF.txt', j)
        i += 1
        process_bar(i, num)
        time.sleep(0.005)

