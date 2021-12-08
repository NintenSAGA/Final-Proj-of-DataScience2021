import sys
import time
from datetime import datetime

from Crawling.crawling import crawl, clear
from Crawling.text_extract import pkulaw_retrieve
from Crawling import common

if __name__ == '__main__':
    crawl(200, 1, 200)
