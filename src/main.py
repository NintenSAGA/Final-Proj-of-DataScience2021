import sys
import time
from datetime import datetime


from NLP.jiebaVersion.jiebaProcessing import cal_word_freq, get_result, parse_word_freq

if __name__ == '__main__':
    # crawl(200, 1, 200)
    with open("/Users/lijiajun/Final-Proj-of-DataScience2021/~Archive/2.刘运宏危险驾驶罪刑事一审刑事判决书.txt") as file:
        text = file.read()
    # 测试NLP，可将待处理文本的路径复制到filepath中，结果位于 src/NLP/jiebaVersion/result.txt
    print(get_result(text))
    # process_property('/Users/lijiajun/Final-Proj-of-DataScience2021/src/NLP/jiebaVersion/accusation_list.txt')
