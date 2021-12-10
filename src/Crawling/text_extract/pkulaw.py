import os

import bs4
from bs4 import BeautifulSoup
from mechanicalsoup import StatefulBrowser


from src.crawling.common import html_path, noise_set, refined_text_path, log
from src.crawling.text_extract import str_insert

browser = None


def import_cookies(cookies: list[dict]):
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


def retrieve_html_file(url: str, counter: int):
    """
    将北大法宝对应文章的文档转换为 html 文件，存入 '/result.txt/~html'

    :param url: 文档链接
    :param counter: 当前计数
    :return:
    """
    global browser

    if browser is None:
        browser = StatefulBrowser()

    browser.open(url)

    with open(html_path.format(counter), 'w') as f:
        f.write(browser.page.prettify())


def anti_anti_crawler(full_text: bs4.Tag):
    '''
    通过探测HTML元素来删除污染信息，已不被使用

    :param full_text:
    :return:
    '''
    for s in full_text.find_all('span'):
        # 删除防爬虫信息
        if s.findChild():
            e = s.findChild()
            noise = str.strip(e.text)
            noise_set.add(noise)
            print(noise + ' deleted')
            e.decompose()

    for s in full_text.find_all('a'):
        # 删除防爬虫信息
        if s.findChild():
            e = s.findChild()
            noise = str.strip(e.text)
            noise_set.add(noise)
            print(noise + ' deleted')
            e.decompose()

    for s in full_text.find_all('a', {'class': 'hide'}):
        # 删除防爬虫信息
        if s.findChild():
            e = s.findChild()
            noise = str.strip(e.text)
            noise_set.add(noise)
            print(noise + ' deleted')
            e.decompose()

    for e in full_text.find_all(['em', 'sup', 'strong', 'small', 'i', 'sub', 'button', 'b']):
        # 删除防爬虫信息
        noise = str.strip(e.text)
        noise_set.add(noise)
        print(noise + ' deleted')
        e.decompose()


def retrieve_text(html_doc: str, counter: int):
    """
    将北大法宝对应文章的html文档转换为 txt 文件，存入 '/result.txt'

    :param html_doc: 文档html
    :param counter: 当前计数
    :return:
    """

    print('正在处理文档......'.format(counter, counter))

    if not os.path.exists(html_doc):
        print('Alert 未找到{}'.format(html_doc))
        return

    with open(html_doc, 'r') as f:
        soup = BeautifulSoup(f.read(), features='html.parser')

    full_text = soup.find('div', {'class', 'fulltext'})

    # anti_anti_crawler(full_text)

    title_tag = full_text.find('p')
    title = str.strip(title_tag.text)
    title_tag.decompose()

    info_tag = full_text.find_all('div')
    info_lines = list(map(lambda x: str.strip(x.text).replace(' ', '').replace('\n\n', ' '), info_tag))
    for i in info_tag:
        i.decompose()

    refined_text = str.strip(full_text.text).replace('\t', '').replace(' ', '').replace('\n', '')

    refined_text = noise_deletion(refined_text)

    found = False
    cut_list = ['判决如下', '附相关法律条文', '判决结', '判决主']
    for words in cut_list:
        idx = refined_text.find(words)
        if idx < 0:
            continue
        found = True
        refined_text = str_insert(refined_text, idx + len(words) + 1, os.linesep)
        refined_text = str_insert(refined_text, idx, os.linesep * 2)

    print('{}.{} retrieved'.format(counter, title) + os.linesep)
    if not os.path.exists(refined_text_path):
        os.mkdir(refined_text_path)
    with open(refined_text_path + '{}.{}.txt'.format(counter, title), 'w') as f:
        f.write(title + os.linesep)
        for info in info_lines:
            f.write(info)
        f.write(os.linesep)
        f.write(refined_text)
    if not found:
        log.append('{}.{} 审判结果未找到'.format(counter, title))


def noise_deletion(refined_text) -> str:
    for noise in noise_set:
        while refined_text.find(noise) >= 0:
            print('Log: {} deleted.'.format(noise))
            refined_text = refined_text.replace(noise, '')
    return refined_text