import os

import requests
from bs4 import BeautifulSoup

from src.crawling.common import result_folder


def gov_retrieve(url: str, counter: int):
    """
    将中华人民共和国最高人民法院公报对应文章的文档转换为 txt 文件，存入 '/result.txt'

    :param counter: 当前计数
    :param url: 文档链接
    :return: null
    """

    print()
    res = ['']
    bs = BeautifulSoup(requests.get(url).content, features='html.parser')

    c = bs.find_all('div', {'class': 'content_box'})[0]

    for cp in c.find_all('p')[1:]:
        prop = cp.get('style')

        if prop is not None and prop.find('center') != -1:
            res[-1] += cp.text.strip()
        else:
            res.append(cp.text)

    with open(result_folder + str(counter) + '.' + res[0] + '.txt', 'w') as f:
        f.write(os.linesep.join(res).replace(chr(0xa0), ' '))

    print('[' + str(counter) + '] Source: ' + url)
    print('Article "' + res[0] + '" has been retrieved.')