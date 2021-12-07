import os
import time
import platform
from sys import stderr

from selenium.webdriver import Edge, ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, WebDriverException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver import EdgeOptions

from src import Crawling
from src.Crawling.text_extract import gov_retrieve
from src.Crawling.text_extract import pkulaw_retrive
from src.Crawling.common import result_folder

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
        print('你妈的，不支持', file=stderr)
        raise NotImplementedError()
    return path


def crawl(n: int = 100, src: int = 1):
    """
    利用 Selenium 扒取裁判文书

    :param n: 要扒取的文件数量
    :param src: 文献来源，0 - 中华人民共和国最高人民法院公报, 1 - 北大法宝
    """

    assert src == 0 or src == 1

    target_site: str
    global counter

    option = EdgeOptions()

    with Edge(executable_path=gimme_path(), options=option) as edge:
        print('Edge Webdriver 已正常启动')
        if src == 0:
            __gov_crawling(n, edge)
        else:
            __pkulaw_crawling(n, edge)


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


def __pkulaw_crawling(n: int, edge: Edge):
    """
    利用 Selenium 扒取北大法宝的裁判文书

    需使用南大ip
    :param n: 要扒取的文件数量
    """
    global counter

    if input('是否要重新获取链接？(y/n): ').startswith('y'):
        __pkulaw_html_crawling(n, edge)
        print('log: 休息十秒')
        time.sleep(10)
    else:
        edge.quit()

    count = 0

    url_list = result_folder + '~url_list.txt'
    with open(url_list, 'r') as f:
        for line in f.read().split('\n'):
            if line.startswith('https'):
                print('log: 开始扒取文件' + str(count))
                pkulaw_retrive(line, count)
                count += 1
                time.sleep(4)


def __pkulaw_html_crawling(n: int, edge: Edge):
    edge.get("https://www.pkulaw.com/case/")

    try:
        login_status = edge.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/a[1]')
        if not login_status.text == '南京大学':
            raise WebDriverException
    except WebDriverException:
        print('登录情况异常，请使用南大网登录或手动登录')
        input('解决后输入任意字符：')

    print('log: 正在筛选条件')

    time.sleep(2)
    # 选择普通案例
    edge.find_element(By.XPATH, "//li[9]/a/span").click()
    print('log: 已选择普通案例')

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
    print('log: 已选择判决书')

    time.sleep(2)
    while True:
        try:
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
    print('log: 已选择刑事一审')

    time.sleep(2)
    while True:
        try:
            # 悬浮每页显示条目
            element = edge.find_element(By.CSS_SELECTOR, ".articleSelect:nth-child(1) h4")
            actions = ActionChains(edge)
            actions.move_to_element(element).perform()
            # 点击每页100条
            edge.find_element(By.XPATH, "//div[3]/div/div[2]/dl/dd[4]").click()
        except ElementNotInteractableException:
            continue
        break
    print('log: 已选择每页100条')

    time.sleep(2)

    # 读取每页所有条目
    count = 0

    url_list = result_folder + '~url_list.txt'
    if os.path.exists(url_list):
        os.remove(url_list)

    while count < n:
        entries = edge.find_elements(By.XPATH, '//*[@id="rightContent"]/div[3]/div/ul/li')
        for e in entries:
            href = e.find_element(By.XPATH, './/div/div/h4/a').get_attribute('href')
            print(href, file=open(url_list, 'a+'))
            print('HTML of entry[' + str(count) + '] retrieved')
            count += 1
            if count == n:
                break
        if not count == n:
            edge.find_element(By.XPATH, '//*[@id="rightContent"]/div[3]/div/div[2]/ul/li[8]/a').click()  # 翻页
            time.sleep(2)

    print('log: 所有条目的链接扒取完毕')

    edge.quit()  # 退出 edge，防止并发

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
