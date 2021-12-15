import os
import sys
import time

from selenium.common.exceptions import WebDriverException, ElementClickInterceptedException, NoSuchElementException, \
    ElementNotInteractableException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver import Edge

from src.crawling.common import result_folder, html_path, log, update_progress_bar, write_msg
from src.crawling.text_extract.pkulaw import import_cookies, retrieve_html_file, retrieve_text, noise_set
from src.crawling import common
from sortedcontainers import SortedSet

counter = 0

pkulaw_url = 'https://www.pkulaw.com/case/'
url_list = common.url_list


def crawl_pkulaw(n: int, edge: Edge, from_n, skip_fu, skip_rhf, year, debug_mode=False, direct_call_mode=False):
    """
    利用 Selenium 扒取北大法宝的裁判文书

    需使用南大ip
    :param direct_call_mode: 直击调用，使用后不退出edge
    :param year: 年份
    :param debug_mode: 只进行url获取
    :param edge:
    :param skip_rhf: skip retrieve html file
    :param skip_fu: skip fetch url
    :param from_n: 从第几份开始
    :param n: 要扒取的文件数量
    """
    global counter, url_list
    url_list = common.url_list.format(year)
    org_len = len(noise_set)
    write_msg("Log: 当前噪音过滤条目{}条".format(org_len))

    if not skip_fu:
        fetch_url(n, edge, from_n, year)
        import_cookies(edge.get_cookies())  # 将selenium的cookies转换给mechanicalsoup
        write_msg('Log: 已完成cookie转换')
        write_msg('Log: 休息十秒')
        if not direct_call_mode:
            for i in range(0, 10):
                update_progress_bar(i, 10, '{}'.format(10 - i))
                time.sleep(1)
            sys.stdout.write('\r0' + os.linesep)
            sys.stdout.flush()
            edge.quit()

    if direct_call_mode or debug_mode:
        return

    count = 0
    with open(url_list, 'r') as f:
        for line in f.read().split('\n'):
            pack = line.split(',')
            date = pack[0]
            title = ''.join(pack[1: -1])
            url = pack[-1]
            name = '{}_{}'.format(date, title)
            if count >= n:
                break
            if not skip_rhf:
                update_progress_bar(count, n, '正在处理 {}'.format(name))
                retrieve_html_file(url, name)
            try:
                ret_msg = retrieve_text(html_path.format(name), name, count)
                update_progress_bar(count, n, ret_msg)
            except Exception:
                write_msg('处理失败！\n')
            count += 1

    # if len(noise_set) != org_len:
    #     log.append('噪音条目由{}条增加至{}条'.format(org_len, len(noise_set)))
    with open(result_folder + 'log.txt', 'w') as l:
        l.write(os.linesep.join(log))


def fetch_url(n: int, edge: Edge, from_n: int = 0, year=2021):
    """
    获取北大法宝网页上的所有url，存于 url_list 文件夹中

    :param year:
    :param n: 文书数量
    :param edge:
    :param from_n:
    :return:
    """
    edge.get("https://www.pkulaw.com/case/")
    n += from_n

    try:
        login_status = edge.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/a[1]')
        if not login_status.text == '南京大学':
            raise WebDriverException
    except WebDriverException:
        write_msg('登录情况异常，请使用南大网登录或手动登录')
        input('解决后输入任意字符：')

    write_msg('Log: 正在筛选条件')

    time.sleep(2)
    # 选择普通案例
    edge.find_element(By.XPATH, "//li[9]/a/span").click()
    write_msg('Log: 已选择普通案例')

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
    write_msg('Log: 已选择判决书')

    time.sleep(2)
    count = 0
    while True:
        try:
            count += 1
            write_msg('Log: 正在尝试选择刑事案件......')
            edge.find_element(By.XPATH, "//div[4]/div/ul/li[2]/a").click()
            time.sleep(2)
            if not edge.find_element(By.XPATH, '//*[@id="rightContent"]/div[2]/div[1]/div/div[1]/a[2]')\
                    .text.startswith('案') and count <= 20:
                continue
            break
        except (WebDriverException, ElementClickInterceptedException, NoSuchElementException):
            if count > 20:
                break
            continue
    write_msg('Log: 已选择刑事案件')

    time.sleep(2)
    while True:
        try:
            write_msg('Log: 正在尝试选择年份......')
            if edge.find_element(By.XPATH, '//*[@id="leftContent"]/div/div[10]/h4/a[1]/i').get_attribute(
                    'class').endswith('c-plus'):
                edge.find_element(By.XPATH, "//div[10]/h4/a/i").click()
            else:
                edge.find_element(By.XPATH, '//div[10]/div/div/a').click()
                time.sleep(1)
                edge.find_element(By.XPATH, "//div[10]/div/ul/li[{}]/a/span".format(2022-year)).click()
                time.sleep(2)
                break
        except (WebDriverException, ElementClickInterceptedException, NoSuchElementException):
            continue
    write_msg('Log: 已选择年份')

    edge.set_window_position(-edge.get_window_size()['width'], 0)

    time.sleep(2)
    manual = True
    for i in range(0, 50):
        try:
            # 悬浮每页显示条目
            write_msg('Log: 正在尝试选择每页100条......')
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
        write_msg('alert: 无法选中，请尝试手动开启每页100条')
        time.sleep(2)
        edge.set_window_position(0, 0)
        time.sleep(5)
        edge.set_window_position(-edge.get_window_size()['width'], 0)
    write_msg('Log: 已选择每页100条')

    time.sleep(2)

    # 读取每页所有条目
    count = 0

    url_set = SortedSet(key=lambda x: date_sort(x))

    try:
        while count < n:
            entries = edge.find_elements(By.XPATH, '//*[@id="rightContent"]/div[3]/div/ul/li')
            for e in entries:
                try:
                    href = e.find_element(By.XPATH, './/div/div/h4/a').get_attribute('href')
                    title = e.find_element(By.XPATH, './/div/div/h4').text
                    date = e.find_element(By.XPATH, './/div/div[2]').text.split('/')[-1]
                except Exception:
                    break
                entry = '{},{},{}'.format(str.strip(date), title, href)
                if entry in url_set:
                    write_msg('重复！')
                    break
                url_set.add(entry)
                update_progress_bar(count, n, '已获取第{}项URL'.format(count))
                count += 1
                if count == n:
                    break
            if not count == n:
                while True:
                    try:
                        edge.find_element(By.XPATH,
                                          '//*[@id="rightContent"]/div[3]/div/div[2]/ul/li[8]/a').click()  # 翻页
                    except WebDriverException:
                        edge.set_window_position(0, 0)
                        write_msg('Log: 疑似出现验证码，请手动操作')
                        time.sleep(0.5)
                        continue
                    break
                time.sleep(2)
        write_msg('Log: 所有条目的链接扒取完毕')
    finally:
        with open(url_list, 'w') as f:
            f.write('\n'.join(url_set))


def date_sort(s: str):
    """
    对诸如 yyyy.mm.dd,nn.[name].txt 格式的字符串拆解key供sorted函数使用

    :param s: 字符串
    :return:
    """
    date_and_n = s.split(',')
    date_vals = date_and_n[0].split('.')

    return date_vals[0], date_vals[1], date_vals[2], date_and_n[1].split('.')[0]
