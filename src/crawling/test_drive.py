from src.crawling import crawl
from src.crawling.core.pkulaw import crawl_pkulaw
from selenium.webdriver import Edge

if __name__ == '__main__':
    # crawl(100, year=2010, debug_mode=True)
    with Edge() as edge:
        for year in range(2012, 2013):
            crawl_pkulaw(n=400, edge=edge, from_n=0, skip_fu=False, skip_rhf=False, year=year, debug_mode=True,
                         direct_call_mode=True)