import os

import bs4
import requests
from bs4 import BeautifulSoup
from mechanicalsoup import StatefulBrowser

from src.Crawling.common import result_folder

browser = None
html_folder = result_folder + '~html/'
html_path = html_folder + '{}.html'


def cookies_import(cookies: list[dict]):
    """
    将 selenium 已有的cookie导入 mechanicalsoup

    :param cookies: cookies字典
    :return: void
    """
    global browser
    if browser is None:
        browser = StatefulBrowser()
    for cookie in cookies:
        c = {cookie['name']: cookie['value']}
        browser.session.cookies.update(c)


def pkulaw_retrieve_html_doc(url: str, counter: int):
    """
    将北大法宝对应文章的文档转换为 html 文件，存入 '/result.txt/~html'

    :param url: 文档链接
    :param counter: 当前计数
    :return:
    """
    global browser
    global html_path

    if browser is None:
        browser = StatefulBrowser()

    browser.open(url)

    with open(html_path.format(counter), 'w') as f:
        f.write(browser.page.prettify())


def anti_anti_crawler(full_text: bs4.Tag):
    for s in full_text.find_all('span'):
        # 删除防爬虫信息
        if s.findChild():
            e = s.findChild()
            print(str.strip(e.text) + ' deleted')
            e.decompose()

    for s in full_text.find_all('a'):
        # 删除防爬虫信息
        if s.findChild():
            e = s.findChild()
            print(str.strip(e.text) + ' deleted')
            e.decompose()

    for e in full_text.find_all(['em', 'sup', 'strong', 'small', 'i', 'sub', 'button']):
        # 删除防爬虫信息
        print(str.strip(e.text) + 'deleted')
        e.decompose()


def str_insert(src: str, idx: int, val: str) -> str:
    return src[:idx] + val + src[idx:]


def pkulaw_retrieve(html_doc: str, counter: int):
    """
    将北大法宝对应文章的html文档转换为 txt 文件，存入 '/result.txt'

    :param html_doc: 文档html
    :param counter: 当前计数
    :return:
    """

    print('正在处理文档......'.format(counter, counter))

    if not os.path.exists(html_doc):
        print('alert: 未找到{}'.format(html_doc))
        return

    with open(html_doc, 'r') as f:
        soup = BeautifulSoup(f.read(), features='html.parser')

    full_text = soup.find('div', {'class', 'fulltext'})
    
    anti_anti_crawler(full_text)

    title_tag = full_text.find('p')
    title = str.strip(title_tag.text)
    title_tag.decompose()

    info_tag = full_text.find_all('div')
    info_lines = list(map(lambda x: str.strip(x.text).replace(' ', '').replace('\n\n', ' '), info_tag))
    for i in info_tag:
        i.decompose()

    refined_text = str.strip(full_text.text).replace(' ', '').replace('\n', '')

    cut_list = ['判决如下：', '附相关法律条文：']
    for words in cut_list:
        idx = refined_text.find(words)
        if idx < 0:
            continue
        refined_text = str_insert(refined_text, idx + len(words), os.linesep)
        refined_text = str_insert(refined_text, idx, os.linesep * 2)

    print('{}.{} retrieved'.format(counter, title) + os.linesep)
    with open(result_folder + str(counter) + '.' + title + '.txt', 'w') as f:
        f.write(title + os.linesep)
        for info in info_lines:
            f.write(info)
        f.write(os.linesep)
        f.write(refined_text)


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
