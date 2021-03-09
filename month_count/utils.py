#encoding: utf-8
import os
import requests
import re
import json
from tqdm import tqdm
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter
import pandas as pd

DFCF_STOCK_REPORT = 'https://data.eastmoney.com/report/stock.jshtml'

def chrome_factory(headless=True, html=DFCF_STOCK_REPORT, wait_policy=10):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    chrome = webdriver.Chrome(options=options)
    chrome.get(html)
    wait = WebDriverWait(chrome, wait_policy)
    return chrome, wait

