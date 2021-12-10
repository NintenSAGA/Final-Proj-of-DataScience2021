import sys
import time
from datetime import datetime

from crawling.core import crawl, clear
from src.crawling.text_extract.pkulaw import retrieve_text
from crawling import common
from NLP.jiebaVersion.jiebaProcessing import calWordFrequency, getResult

if __name__ == '__main__':
    # crawl(200, 1, 200)

    # 测试NLP，可将待处理文本的路径复制到filepath中，结果位于 src/NLP/jiebaVersion/result.txt
    filepath = '/Users/lijiajun/Final-Proj-of-DataScience2021/~retrieved/1.雷某帮助信息网络犯罪活动罪、帮助信息网络犯罪活动罪刑事一审刑事判决书.txt'
    cal_word_frequency(filepath)
    get_result('/Users/lijiajun/Final-Proj-of-DataScience2021/src/NLP/jiebaVersion/wF.txt')

