import jieba
import re
import jieba.posseg as pseg

# 全国法院名单
jieba.load_userdict('src/NLP/jiebaVersion/全国法院名单')

# 其他需要增加权重的词语
jieba.load_userdict('src/NLP/jiebaVersion/userdict')


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


def calWordFrequency(text):
    """
        获得分词后每个词的词性以及词频，并按词性分类，按词频排序，并写入 wF.txt

        :parameter text：待切割的文本
    """
    wordFrequency = {}
    with open('src/NLP/jiebaVersion/wF.txt', 'w') as wFfile:
        for line in text:
            for word in line:
                if wordFrequency.get(str(word)):
                    wordFrequency[str(word)] += 1
                else:
                    wordFrequency[str(word)] = 1

        sortedwordFrequency = sorted(wordFrequency.items(), key=lambda x: x[1], reverse=True)
        for word in sortedwordFrequency:
            wFfile.write(str(word) + '\n')
    wFfile.close()


def getResult(wFfilepath):
    """
        计算得到结果

        :param wFfilepath: 词频文本目录
        :return: 得到文本分析结果
    """
