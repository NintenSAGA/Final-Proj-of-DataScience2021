import os
import sys
import time

from selenium.common.exceptions import WebDriverException, ElementClickInterceptedException, NoSuchElementException, \
    ElementNotInteractableException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver import Edge

from src.crawling.common import result_folder, html_folder, html_path, log
from src.crawling.text_extract.pkulaw import import_cookies, retrieve_html_file, retrieve_text
counter = 0

pkulaw_url = 'https://www.pkulaw.com/case/'


def crawl_pkulaw(n: int, edge: Edge, from_page: int = 0,
                 skip_url_fetch: bool = False, skip_html_retrieve: bool = False):
    """
    利用 Selenium 扒取北大法宝的裁判文书

    需使用南大ip
    :param skip_html_retrieve:
    :param skip_url_fetch:
    :param from_page:
    :param edge:
    :param n: 要扒取的文件数量
    """
    global counter
    url_list = result_folder + '~url_list.txt'

    if not os.path.exists(url_list) or input('是否要重新获取链接？(y/n): ').startswith('y'):
        fetch_url(n, edge, from_page)
        import_cookies(edge.get_cookies())  # 将selenium的cookies转换给mechanicalsoup
        print('Log: 已完成cookie转换')
        print('Log: 休息十秒')
        for i in range(0, 10):
            sys.stdout.write('\r{}'.format(10 - i))
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write('\r0' + os.linesep)
        sys.stdout.flush()

    edge.quit()

    if not os.path.exists(html_folder):
        os.mkdir(html_folder)
    else:
        if len(os.listdir(html_folder)) >= n:
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
                    retrieve_html_file(line, count)
                try:
                    retrieve_text(html_path.format(count), count)
                except Exception:
                    print('处理失败！\n')
                count += 1
    with open(result_folder + 'log.txt', 'w') as l:
        l.write(os.linesep.join(log))


def fetch_url(n: int, edge: Edge, from_page: int = 0):
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