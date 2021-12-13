import os
import platform

from selenium.webdriver import Edge

from src import crawling
from src.crawling import common
from src.crawling.common import result_folder, html_folder, refined_text_folder, url_list, html_path, write_msg
from src.crawling.core import crawl_pkulaw


def crawl(n, src: int = 1, from_n: int = 0,
          skip_fu: bool = None, skip_rhf: bool = None,
          launched_by_GUI: bool = False):
    """
    利用 Selenium 扒取裁判文书

    :param launched_by_GUI:
    :param skip_rhf: skip retrieve html file
    :param skip_fu: skip fetch url
    :param from_n: 从第几份开始
    :param n: 要扒取的文件数量
    :param src: 文献来源，0 - 中华人民共和国最高人民法院公报, 1 - 北大法宝
    """

    assert src == 0 or src == 1

    common.launched_by_GUI = launched_by_GUI

    # 确认路径存在
    for folder in [result_folder, html_folder, refined_text_folder]:
        if not os.path.exists(folder):
            os.mkdir(folder)

    # 检查url_list是否存在
    fu_can_skip = os.path.exists(url_list)

    # 检查html文件缓存
    rhf_can_skip: bool
    if len(os.listdir(html_folder)) > 0:
        rhf_can_skip = True
        write_msg('Log: 已存在html文档缓存，正在核验完整性......')
        for i in range(0, n):
            if not os.path.exists(html_path.format(i)):
                write_msg('alert: 第{}项缺失！'.format(i))
    else:
        rhf_can_skip = False

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
    elif src == 1:
        crawl_pkulaw(n, edge, from_n, skip_fu, skip_rhf)

    if edge is not None:
        edge.quit()


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
