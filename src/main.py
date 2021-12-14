import sys
import time
from datetime import datetime


from NLP.jiebaVersion.jiebaProcessing import cal_word_frequency, get_result, process_property

if __name__ == '__main__':
    # crawl(200, 1, 200)

    # 测试NLP，可将待处理文本的路径复制到filepath中，结果位于 src/NLP/jiebaVersion/result.txt
    get_result('/Users/lijiajun/Final-Proj-of-DataScience2021/~Archive', 10)
    # process_property('/Users/lijiajun/Final-Proj-of-DataScience2021/src/NLP/jiebaVersion/罪名.txt')
