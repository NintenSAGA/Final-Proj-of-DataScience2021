import platform
import time
from sys import stderr

from selenium.webdriver import Edge
from selenium.webdriver.common.by import By

from src import Crawling

import os

import requests
from bs4 import BeautifulSoup

folder = Crawling.__path__[0] + '/results/'
target_site = 'http://gongbao.court.gov.cn/QueryArticle.html?title=&content=&document_number=&serial_no=cpwsxd&year=-1&number=-1'
counter = 0


def gimme_path() -> str:
    """ 检查系统类型，获取相应版本的 Edge webdriver 运行路径。
        目前仅支持 macOS 和 Windows

        :return: executable_path
    """
    path: str
    os_type = platform.system()
    if os_type == 'Darwin':
        print('运行系统为macOS')
        path = Crawling.__path__[0] + '/Webdriver/Edge/msedgedriver'
    elif os_type == 'Windows':
        print('运行系统为Windows')
        path = Crawling.__path__[0] + '/Webdriver/Edge/msedgedriver.exe'
    else:
        print('你妈的，不支持', file=stderr)
        raise NotImplementedError()
    return path


def retrieve(url: str):
    """
    将对应文章的文档转换为 txt 文件，存入 '/result'

    :param url: 文档链接
    :return: null
    """

    global counter
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

    with open(folder + str(counter) + '.' + res[0] + '.txt', 'w') as f:
        f.write(os.linesep.join(res).replace(chr(0xa0), ' '))

    print('[' + str(counter) + '] Source: ' + url)
    print('Article "' + res[0] + '" has been retrieved.')
    counter += 1


def crawl(n: int = 100):
    """
    利用 Selenium 扒取中华人民共和国最高人民法院公报的裁判文书

    :param n: 要扒取的文件数量
    """

    global target_site
    global counter

    with Edge(executable_path=gimme_path()) as edge:
        edge.get(target_site)

        while counter < n:
            entries = edge.find_elements(By.XPATH, '//*[@id="datas"]/li')
            for i in range(1, len(entries)):
                entry = entries[i]
                target_site = entry.find_element(By.XPATH, './/span/a').get_attribute('href')
                retrieve(target_site)
            edge.find_element(By.XPATH, '//*[@id="pager"]/a[4]').click()
            time.sleep(2)


def clear():
    """
    删除'/results/'中的所有文件

    :return:
    """
    if input('确定要删除所有缓存文件吗？(y/n): ').startswith('y'):
        if len(os.listdir(folder)) == 0:
            print('都没文件了哥哥')
            return
        for file_name in os.listdir(folder):
            print(file_name + ' is deleted')
            os.remove(folder + file_name)
