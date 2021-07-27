#encoding: utf-8
import os, sys

from month_count.main import MonthCount

if __name__ == '__main__':
    days = sys.argv[1]
    days = int(days)
    counter = MonthCount(headless=True, days=days)
    counter.start()