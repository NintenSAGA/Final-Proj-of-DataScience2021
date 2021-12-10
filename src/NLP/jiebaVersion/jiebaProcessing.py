import jieba
import re
import jieba.posseg as pseg

# 全国法院名单.txt
jieba.load_userdict('/Users/lijiajun/Final-Proj-of-DataScience2021/src/NLP/jiebaVersion/全国法院名单.txt')

# 罪名.txt
jieba.load_userdict('/Users/lijiajun/Final-Proj-of-DataScience2021/src/NLP/jiebaVersion/罪名.txt')

# 其他需要增加权重的词语
jieba.load_userdict('/Users/lijiajun/Final-Proj-of-DataScience2021/src/NLP/jiebaVersion/userdict.txt')


def getVerdict(filepath):
    """ 根据文本格式，获得判决结果

        :parameter filepath:文档路径
        :return Verdict
    """
    with open(filepath, 'r') as file:
        lines = file.read().split('\n')
        temp = 0
        for i in range(len(lines)):
            if "判决如下" in lines[i]:
                temp = i
                break

    return lines[temp+1]


def posProcess(filePath):
    # 处理字典词性
    with open(filePath, 'r+') as file:
        text = file.read()
        lineList = text.split('\n')

    with open(filePath, 'w+') as file:
        for line in lineList:
            file.write(''.join(line+' cg'+'\n'))

    file.close()


def textProcessing(filepath):
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


def calWordFrequency(filepath):
    """
        获得分词后每个词的词性以及词频，并按词性分类，按词频排序，并写入 wF.txt

        :parameter tex(list)：待切割的文本
    """
    text = textProcessing(filepath)
    verdict = getVerdict(filepath)
    wordFrequency = {}
    with open('/Users/lijiajun/Final-Proj-of-DataScience2021/src/NLP/jiebaVersion/wF.txt', 'w') as wFfile:
        for line in text:
            for word in line:
                if wordFrequency.get(str(word)):
                    wordFrequency[str(word)] += 1
                else:
                    wordFrequency[str(word)] = 1

        sortedwordFrequency = sorted(wordFrequency.items(), key=lambda x: x[1], reverse=True)
        wFfile.write('(\''+verdict + '/re' + '\')'+'\n')
        for word in sortedwordFrequency:
            wFfile.write(str(word) + '\n')
    wFfile.close()


def getResult(wFfilepath):
    """
        计算得到结果

        :param wFfilepath: 词频文本目录
        :return: 得到文本分析结果
    """
    # 个人基本信息
    personInfo = ["姓名："]

    # 地区
    area = ["地区:"]

    # 罪名
    case_cause = ["罪名："]

    # 审理法院
    court = ["法院："]

    # 判决结果
    sentences = ["判决结果："]

    # 涉案金额
    money = ["涉案金额："]

    # 危险驾驶相关信息
    dan_message = ["危险驾驶："]
    with open(wFfilepath, 'r+') as wFfile:
        for line in wFfile:
            line = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", " ", line)
            line = line.strip().replace('  ', ' ')
            words = line.split(" ")
            if words[1] == 'nr':
                personInfo.append(words[0])
            elif words[1] == 'ct':
                court.append(words[0])
            elif words[1] == 'ns':
                area.append(words[0])
            elif words[1] == 'cg':
                case_cause.append(words[0])
            elif words[len(words)-1] == 're':
                for word in words:
                    if word != 're':
                        sentences.append('\n\t' + word)

    with open('/Users/lijiajun/Final-Proj-of-DataScience2021/src/NLP/jiebaVersion/result.txt', 'w') as resultfile:
        resultfile.write(toString(personInfo) + '\n')
        resultfile.write(toString(area) + '\n')
        resultfile.write(toString(case_cause) + '\n')
        resultfile.write(toString(court) + '\n')
        resultfile.write(toString(sentences) + '\n')
        resultfile.write(toString(money) + '\n')
        resultfile.write(toString(dan_message) + '\n')


def toString(s):
    res = ""
    for word in s:
        res += (word + ' ')
    return res
