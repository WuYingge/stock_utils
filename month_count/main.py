#encoding: utf-8
import sys, os
import pandas as pd
from copy import deepcopy
sys.path.append(os.getcwd())
from datetime import datetime, timedelta
from month_count.utils import chrome_factory



class MonthCount(object):
    DFCF_STOCK_REPORT = 'https://data.eastmoney.com/report/stock.jshtml'
    def __init__(self, 
                 days=30,
                 headless=True, 
                 html=DFCF_STOCK_REPORT, 
                 wait_policy=10
                 ):
        self.chrome, self.wait = chrome_factory(headless=headless,html=html, wait_policy=wait_policy)
        self.data = pd.DataFrame(
            columns=['date', 'name', 'symbol', 'count']
        )
        self.date_period = timedelta(days=days)
        self.chrome.implicitly_wait(20)
        
    def start(self):
        now = datetime.utcnow() + timedelta(hours=8)
        farest_date = now - self.date_period
        from collections import Counter
        symbol_list = []
        symbol_company_mapper = {}
        table = self.chrome.find_element_by_css_selector('#stock_table .table-model')
        trs = table.find_elements_by_tag_name('tr')
        time = trs[-1].find_element_by_css_selector('td:nth-child(15)').text
        time = datetime.strptime(time, '%Y-%m-%d')
        while time >= farest_date:
            for tr in trs:
                if '详细  股吧' not in tr.text:
                    continue
                time = tr.find_element_by_css_selector('td:nth-child(15)').text
                time = datetime.strptime(time, '%Y-%m-%d')
                if time >= farest_date:
                    symbol = tr.find_element_by_css_selector('td:nth-child(2)').text
                    symbol_list.append(symbol)
                    symbol_company_mapper.update(
                        {symbol: tr.find_element_by_css_selector('td:nth-child(3)').text}
                    )
                else:
                    break
            if not time >= farest_date:
                print(time)
                break
            navigators = self.chrome.find_elements_by_css_selector('#stock_table_pager > div.pagerbox > a')
            next_page = None
            for button in navigators:
                if '下一页' in button.text:
                    next_page = button
                    break
            if not button:
                raise Exception('next_page not found but' + button.text)
            next_page.click()
            table = self.chrome.find_element_by_css_selector('#stock_table .table-model')
            trs = table.find_elements_by_tag_name('tr')
        
                
        counter = Counter(symbol_list).most_common()
        dict_list = []
        for symbol, count in counter:
            temp_dict = {
                'symbol': symbol,
                'company': symbol_company_mapper.get(symbol),
                'count': count
            }
            dict_list.append(temp_dict)
        fp = f"data/{self.date_period.days}"
        fname = f"{now.strftime('%Y-%m-%d')}.xlsx"
        if not os.path.exists(fp):
            os.mkdir(fp)
        whole_fp = os.path.join(fp, fname)
        
        pd.DataFrame(dict_list).to_excel(whole_fp, index=False, header=True, encoding='utf-8_sig')
        
            
