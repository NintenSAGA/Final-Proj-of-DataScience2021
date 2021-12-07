import os

import requests
from bs4 import BeautifulSoup
from mechanicalsoup import StatefulBrowser

from src.Crawling.common import result_folder
import re

browser = None


def pkulaw_retrive(url: str, counter: int):
    """
    将北大法宝对应文章的文档转换为 txt 文件，存入 '/result'

    :param url: 文档链接
    :param counter: 当前计数
    :return:
    """
    print()
    global browser
    if browser is None:
        browser = StatefulBrowser()

    browser.open(url)
    soup = browser.page

    for e in soup.find_all('em', {'class': 'copyright'}):
        # 删除防爬虫信息
        print(e.text + 'deleted')
        e.decompose()

    for e in soup.find_all('sup', {'class': 'catch'}):
        # 删除防爬虫信息
        print(e.text + 'deleted')
        e.decompose()

    for e in soup.find_all('em', {'class': 'random'}):
        # 删除防爬虫信息
        print(e.text + 'deleted')
        e.decompose()

    refined_text = soup.find('div', {'class': 'fulltext'}).text\
        .replace('\n', '')\
        .replace('\u3000', '\n')\
        .replace('\n\n', '\n')  # type: str

    match = re.match(r'^[^判决书]*判决书', refined_text)
    title = match.group()

    refined_text = refined_text[:match.end()] + '\n' + refined_text[match.end():]

    print('[{}] {} retrieved'.format(counter, title))
    print(refined_text, file=open(result_folder + str(counter) + '.' + title + '.txt', 'w'))


def gov_retrieve(url: str, counter: int):
    """
    将中华人民共和国最高人民法院公报对应文章的文档转换为 txt 文件，存入 '/result'

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