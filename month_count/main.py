#encoding: utf-8
import sys, os
import pandas as pd
from copy import deepcopy
sys.path.append(os.getcwd())
from datetime import datetime, timedelta
from month_count.utils import chrome_factory

DFCF_STOCK_REPORT = 'https://data.eastmoney.com/report/stock.jshtml'

class MonthCount(object):
    
    def __init__(self, 
                 days=30,
                 headless=True, 
                 html=DFCF_STOCK_REPORT, 
                 wait_policy=10
                 ):
        self.chrome, self.wait = chrome_factory(headless=headless,html=html, wait_policy=10)
        self.data = pd.DataFrame(
            columns=['No', 'symbol', 'company', 'report_name', 'rate', 
                     'rate_change', 'institute', 'origin_count', 'industry', 'date']
        )
        self.date_period = timedelta(days=30)
        
    def start(self):
        now = datetime.utcnow() + timedelta(hours=8)
        this_time = deepcopy(now)
        while now - this_time <= self.date_period:
            table = chrome.find_element_by_css_selector('#industry_table')
            #TODO 完整逻辑