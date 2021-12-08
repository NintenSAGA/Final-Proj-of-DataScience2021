from Crawling.crawling import crawl, clear
from Crawling.text_extract import pkulaw_retrive
from Crawling import common

from NLP.jiebaVersion.jiebaProcessing import textProcessing,calWordFrequency,getResult
if __name__ == '__main__':
    calWordFrequency(textProcessing('/Users/lijiajun/Final-Proj-of-DataScience2021/~retrieved/1.雷某帮助信息网络犯罪活动罪、帮助信息网络犯罪活动罪刑事一审刑事判决书.txt'))

