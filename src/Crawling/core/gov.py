import time

from selenium.webdriver.common.by import By
from selenium.webdriver import Edge

from src.crawling.text_extract.gov import gov_retrieve

gov_url = 'http://gongbao.court.gov.cn/QueryArticle.html?title=&content=&document_number=&serial_no=cpwsxd&year=-1&number=-1'
counter = 0


def __crawl_gov(n: int, edge: Edge):
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