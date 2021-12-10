import os
import platform

from selenium.webdriver import Edge

from src import crawling
from src.crawling.core.gov import __crawl_gov
from src.crawling.core.pkulaw import crawl_pkulaw
from src.crawling.common import result_folder
counter = 0


def crawl(n: int = 100, src: int = 1, from_page: int = 0,
          skip_url_fetch: bool = False, skip_html_retrieve: bool = False):
    """
    利用 Selenium 扒取裁判文书

    :param skip_html_retrieve:
    :param skip_url_fetch:
    :param from_page: 从第几份开始
    :param n: 要扒取的文件数量
    :param src: 文献来源，0 - 中华人民共和国最高人民法院公报, 1 - 北大法宝
    """

    assert src == 0 or src == 1

    target_site: str
    global counter

    with Edge(executable_path=__get_webdriver_path()) as edge:
        print('Edge Webdriver 已正常启动')
        edge.set_window_position(-edge.get_window_size()['width'], 0)
        if src == 0:
            __crawl_gov(n, edge)
        else:
            crawl_pkulaw(n, edge, from_page, skip_url_fetch, skip_html_retrieve)


def __get_webdriver_path() -> str:
    """ 检查系统类型，获取相应版本的 Edge webdriver 运行路径。
        目前仅支持 macOS 和 Windows

        :return: executable_path
    """
    path: str
    os_type = platform.system()
    if os_type == 'Darwin':
        print('运行系统为macOS')
        path = crawling.__path__[0] + '/Webdriver/Edge/msedgedriver'
    elif os_type == 'Windows':
        print('运行系统为Windows')
        path = crawling.__path__[0] + '/Webdriver/Edge/msedgedriver.exe'
    else:
        print('Log：暂不支持此系统')
        raise NotImplementedError()
    return path


def clear():
    """
    删除'/results/'中的所有文件

    :return:
    """
    if input('确定要删除所有缓存文件吗？(y/n): ').startswith('y'):
        if len(os.listdir(result_folder)) <= 1:
            print('都没文件了哥哥')
            return
        for file_name in os.listdir(result_folder):
            if file_name.startswith('~'):
                continue
            print(file_name + ' is deleted')
            os.remove(result_folder + file_name)
