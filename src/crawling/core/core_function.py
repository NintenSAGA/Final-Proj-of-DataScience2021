import os
import platform

from selenium.webdriver import Edge

from src import crawling
from src.crawling import common
from src.crawling.common import result_folder, html_folder, refined_text_folder, html_path, write_msg
from src.crawling.core import crawl_pkulaw

url_list = common.url_list


def crawl(n, src: int = 1, year: int = 2021, from_n: int = 0,
          skip_fu: bool = None, skip_rhf: bool = None,
          launched_by_gui: bool = False, debug_mode=False):
    """
    利用 Selenium 扒取裁判文书

    :param debug_mode:
    :param year: 年份
    :param launched_by_gui:
    :param skip_rhf: skip retrieve html file
    :param skip_fu: skip fetch url
    :param from_n: 从第几份开始
    :param n: 要扒取的文件数量
    :param src: 文献来源，1 - 北大法宝
    """

    assert src == 0 or src == 1

    global url_list

    common.launched_by_GUI = launched_by_gui
    url_list = common.url_list.format(year)

    # 确认路径存在
    for folder in [result_folder, html_folder, refined_text_folder]:
        if not os.path.exists(folder):
            os.mkdir(folder)

    fu_can_skip, msg = check_url_list(from_n, n, year)
    write_msg(msg)

    # 检查html文件缓存
    rhf_can_skip, msg = check_html_list(from_n, n, year)
    write_msg(msg)

    if not launched_by_gui and skip_fu is None and skip_rhf is None:
        skip_fu = input('是否跳过fetch_url: ').startswith('y')
        skip_rhf = input('是否跳过retrieve_html_file: ').startswith('y')

    # 检查输入参数合法性
    if not skip_fu and skip_rhf:
        write_msg('Error: 在重新获取url_list的情况下不可跳过html文件获取！')
        return
    if skip_fu and not fu_can_skip:
        write_msg('Error: 不存在url_list，不可跳过fetch_url')
        return
    if skip_rhf and not rhf_can_skip:
        write_msg('Error: 不存在html缓存，不可跳过retrieve_html_file')

    # 未设定时，由用户自行选择
    if skip_fu is None:
        if not fu_can_skip:
            skip_fu = False
            write_msg('Log: 不存在url_list，不跳过fetch_url')
        else:
            write_msg('Alert: 未设置是否跳过fetch_url')
            skip_fu = input('是否要跳过？(y/n): ').startswith('y')

        if skip_fu and skip_rhf is None:
            if rhf_can_skip:
                write_msg('Alert: 未设置是否跳过retrieve_html_file')
                skip_rhf = input('是否要跳过？(y/n): ').startswith('y')
            else:
                write_msg('Log: 不存在html缓存，不跳过retrieve_html_file')
                skip_rhf = False
        elif not skip_fu:
            skip_rhf = False
            write_msg('Log: fetch_url与retrieve_html_file均不跳过')

    # 正式开始执行
    if not skip_fu:
        edge = Edge(executable_path=get_webdriver_path())
        write_msg('Log: Edge Webdriver 已正常启动')
        edge.set_window_position(-edge.get_window_size()['width'], 0)
    else:
        edge = None
        write_msg('Log: Edge Webdriver 不启动')

    if src == 0:
        write_msg('Error: 本源暂停使用')
        return
        # crawl_gov(n, edge)

    crawl_pkulaw(n, edge, from_n, skip_fu, skip_rhf, year, debug_mode)

    if edge is not None:
        edge.quit()


def check_html_list(from_n, n, year=2021) -> (bool, str):
    rhf_can_skip: bool
    existed = 0
    msg: str
    
    if not os.path.exists(html_folder):
        os.mkdir(html_folder)

    if len(os.listdir(html_folder)) > 0:
        for file in os.listdir(html_folder):
            if file.startswith(str(year)):
                existed += 1

    if existed != 0:
        rhf_can_skip = True
        if existed >= n:
            msg = 'Log: 存在html文档缓存，含完整{}份'.format(n)
        else:
            msg = 'Log: html缓存不完整，缺失{}份'.format(n - existed)
    else:
        rhf_can_skip = False
        msg = 'Log: 不存在html缓存'

    return rhf_can_skip, msg


def check_url_list(from_n, n, year=None) -> (bool, str):
    # 检查url_list是否存在
    global url_list
    if year is not None:
        url_list = common.url_list.format(year)
    mis: int
    existed = 0
    msg: str
    fu_can_skip = os.path.exists(url_list)
    if fu_can_skip:
        with open(url_list, 'r') as f:
            for _ in f.readlines():
                existed += 1
        mis = max(0, n - existed)
        if mis == 0:
            msg = 'Log: 存在url_list缓存，含完整{}份'.format(n)
        else:
            msg = 'Log: url_list缓存不完整，缺失{}份'.format(mis)
    else:
        msg = 'Log: 不存在url_list缓存'

    return fu_can_skip, msg


def get_webdriver_path() -> str:
    """ 检查系统类型，获取相应版本的 Edge webdriver 运行路径。
        目前仅支持 macOS 和 Windows

        :return: executable_path
    """
    path: str
    os_type = platform.system()
    if os_type == 'Darwin':
        write_msg('运行系统为macOS')
        path = crawling.__path__[0] + '/Webdriver/Edge/msedgedriver'
    elif os_type == 'Windows':
        write_msg('运行系统为Windows')
        path = crawling.__path__[0] + '/Webdriver/Edge/msedgedriver.exe'
    else:
        write_msg('Log：暂不支持此系统')
        raise NotImplementedError()
    return path


def clear():
    """
    删除'/results/'中的所有文件

    :return:
    """
    if input('确定要删除所有缓存文件吗？(y/n): ').startswith('y'):
        if len(os.listdir(result_folder)) <= 1:
            write_msg('都没文件了哥哥')
            return
        for file_name in os.listdir(result_folder):
            if file_name.startswith('~'):
                continue
            write_msg(file_name + ' is deleted')
            os.remove(result_folder + file_name)
