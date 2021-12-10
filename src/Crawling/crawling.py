import os
import sys
import time
import platform
import pickle

from selenium.webdriver import Edge, ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, WebDriverException, NoSuchElementException, \
    ElementNotInteractableException

from src import Crawling
from src.Crawling import text_extract
from src.Crawling.text_extract import gov_retrieve
from src.Crawling.text_extract import pkulaw_text_retrieve
from src.Crawling.text_extract import cookies_import
from src.Crawling.text_extract import pkulaw_html_file_retrieve
from src.Crawling.common import result_folder
from src.Crawling.text_extract import html_path
from src.Crawling.common import log

gov_url = 'http://gongbao.court.gov.cn/QueryArticle.html?title=&content=&document_number=&serial_no=cpwsxd&year=-1&number=-1'
pkulaw_url = 'https://www.pkulaw.com/case/'
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
        print('Log：暂不支持此系统')
        raise NotImplementedError()
    return path


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

    with Edge(executable_path=gimme_path()) as edge:
        print('Edge Webdriver 已正常启动')
        edge.set_window_position(-edge.get_window_size()['width'], 0)
        if src == 0:
            __gov_crawling(n, edge)
        else:
            __pkulaw_crawling(n, edge, from_page, skip_url_fetch, skip_html_retrieve)


def __gov_crawling(n: int, edge: Edge):
    """
    利用 Selenium 扒取中华人民共和国最高人民法院公报的裁判文书
    :param n: 要扒取的文件数量
    """
    target_site = gov_url
    global counter

    edge.get(target_site)

    while counter < n:
        entries = edge.find_elements(By.XPATH, '//*[@id="datas"]/li')
        for i in range(1, min(len(entries), n - counter + 1)):
            entry = entries[i]
            target_site = entry.find_element(By.XPATH, './/span/a').get_attribute('href')
            gov_retrieve(target_site, counter)
            counter += 1
        if not counter >= n:
            edge.find_element(By.XPATH, '//*[@id="pager"]/a[4]').click()
            time.sleep(2)


def __pkulaw_crawling(n: int, edge: Edge, from_page: int = 0,
                      skip_url_fetch: bool = False, skip_html_retrieve: bool = False):
    """
    利用 Selenium 扒取北大法宝的裁判文书

    需使用南大ip
    :param n: 要扒取的文件数量
    """
    global counter
    url_list = result_folder + '~url_list.txt'
    text_extract.noise_set = pickle.load(open(result_folder + '~noise_set.pkl', 'rb'))

    if not os.path.exists(url_list) or input('是否要重新获取链接？(y/n): ').startswith('y'):
        __pkulaw_url_fetch(n, edge, from_page)
        cookies_import(edge.get_cookies())  # 将selenium的cookies转换给mechanicalsoup
        print('Log: 已完成cookie转换')
        print('Log: 休息十秒')
        for i in range(0, 10):
            sys.stdout.write('\r{}'.format(10 - i))
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write('\r0' + os.linesep)
        sys.stdout.flush()

    edge.quit()

    if not os.path.exists(text_extract.html_folder):
        os.mkdir(text_extract.html_folder)
    else:
        if len(os.listdir(text_extract.html_folder)) >= n:
            print('Log: 已存在html文档缓存，正在核验完整性......')
            for i in range(0, n):
                if not os.path.exists(html_path.format(i)):
                    print('alert: 第{}项缺失！'.format(i))
            skip_html_retrieve = input('是否要跳过html页面获取，直接载入已有文档？(y/n): ').startswith('y')

    count = 0
    with open(url_list, 'r') as f:
        for line in f.read().split('\n'):
            if line.startswith('https'):
                if count < from_page:
                    count += 1
                    continue
                print('[{}]============================'.format(count))
                if not skip_html_retrieve:
                    pkulaw_html_file_retrieve(line, count)
                try:
                    pkulaw_text_retrieve(html_path.format(count), count)
                except Exception:
                    print('处理失败！\n')
                count += 1
    with open(result_folder + 'log.txt', 'w') as l:
        l.write(os.linesep.join(log))


def __pkulaw_url_fetch(n: int, edge: Edge, from_page: int = 0):
    edge.get("https://www.pkulaw.com/case/")
    n += from_page

    try:
        login_status = edge.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/a[1]')
        if not login_status.text == '南京大学':
            raise WebDriverException
    except WebDriverException:
        print('登录情况异常，请使用南大网登录或手动登录')
        input('解决后输入任意字符：')

    print('Log: 正在筛选条件')

    time.sleep(2)
    # 选择普通案例
    edge.find_element(By.XPATH, "//li[9]/a/span").click()
    print('Log: 已选择普通案例')

    time.sleep(2)
    while True:
        try:
            if edge.find_element(By.XPATH, '//*[@id="leftContent"]/div/div[9]/h4/a[1]/i').get_attribute(
                    'class').endswith('c-plus'):
                edge.find_element(By.XPATH, "//div[9]/h4/a/i").click()
            else:
                edge.find_element(By.XPATH, "//div[9]/div/ul/li/a/span").click()
                time.sleep(2)
                break
        except (WebDriverException, ElementClickInterceptedException, NoSuchElementException):
            continue
    print('Log: 已选择判决书')

    edge.set_window_position(0, 0)
    time.sleep(2)
    while True:
        try:
            print('Log: 正在尝试选择刑事一审......')
            if edge.find_element(By.XPATH, '//*[@id="CaseClassport_9_switch"]').get_attribute('class').endswith(
                    'close'):
                edge.find_element(By.XPATH, "//div[4]/div/ul/li[2]/span").click()
            else:
                edge.find_element(By.XPATH, "//li[2]/ul/li/a/span").click()
                time.sleep(2)
            if not edge.find_element(By.XPATH,
                                         '//*[@id="rightContent"]/div[2]/div[1]/div/div[1]/a[2]').text.startswith('案'):
                continue
            break
        except (WebDriverException, ElementClickInterceptedException, NoSuchElementException):
            continue
    print('Log: 已选择刑事一审')

    edge.set_window_position(-edge.get_window_size()['width'], 0)

    time.sleep(2)
    manual = True
    for i in range(0, 50):
        try:
            # 悬浮每页显示条目
            print('Log: 正在尝试选择每页100条......')
            element = edge.find_element(By.CSS_SELECTOR, ".articleSelect:nth-child(1) h4")
            actions = ActionChains(edge)
            actions.move_to_element(element).perform()
            # 点击每页100条
            edge.find_element(By.XPATH, "//div[3]/div/div[2]/dl/dd[4]").click()
        except ElementNotInteractableException:
            continue
        manual = False
        break
    if manual:
        print('alert: 无法选中，请尝试手动开启每页100条')
        time.sleep(2)
        edge.set_window_position(0, 0)
        input('完成手动操作后输入任意键：')
        edge.set_window_position(-edge.get_window_size()['width'], 0)
    print('Log: 已选择每页100条')

    time.sleep(2)

    # 读取每页所有条目
    count = 0

    url_list = result_folder + '~url_list.txt'

    url_set = set()
    while count < n:
        entries = edge.find_elements(By.XPATH, '//*[@id="rightContent"]/div[3]/div/ul/li')
        for e in entries:
            href = e.find_element(By.XPATH, './/div/div/h4/a').get_attribute('href')
            if href in url_set:
                print('重复！')
                break
            url_set.add(href)
            print('HTML of entry[' + str(count) + '] retrieved')
            count += 1
            if count == n:
                break
        if not count == n:
            while True:
                try:
                    edge.find_element(By.XPATH, '//*[@id="rightContent"]/div[3]/div/div[2]/ul/li[8]/a').click()  # 翻页
                except WebDriverException:
                    edge.set_window_position(0, 0)
                    print('Log: 疑似出现验证码，请手动操作')
                    time.sleep(0.5)
                    continue
                break
            time.sleep(2)
    print('Log: 所有条目的链接扒取完毕')
    with open(url_list, 'w') as f:
        f.write('\n'.join(url_set))


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
