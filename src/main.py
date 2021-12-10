import sys
import time
from datetime import datetime

from Crawling.crawling import crawl, clear
from Crawling.text_extract import pkulaw_text_retrieve
from Crawling import common
from NLP.jiebaVersion.jiebaProcessing import calWordFrequency, getResult

if __name__ == '__main__':
    # crawl(200, 1, 200)
    calWordFrequency('/Users/lijiajun/Final-Proj-of-DataScience2021/~retrieved/2.刘运宏危险驾驶罪刑事一审刑事判决书.txt')
    getResult('/Users/lijiajun/Final-Proj-of-DataScience2021/src/NLP/jiebaVersion/wF.txt')

