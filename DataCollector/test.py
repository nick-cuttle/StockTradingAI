import requests
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, date2num
from mplfinance.original_flavor import candlestick_ohlc
from mplfinance import plot
import matplotlib.dates as mpdates
import pandas as pd
import datetime
import json
import random
from camera import Camera
import argparse
import sys
import time
import gc
import pathlib

url = "https://financialmodelingprep.com/api/v3/historical-chart/4hour/AAPL?from=2023-08-10&to=2023-09-10&apikey=J6wnkSNzZpMvfBqBORVBxjMjhLrZQ7lX"
i = 0

FROM_DATE = "2004-01-01"
TO_DATE = "2004-01-03"
OG_FROM_DATE = "2004-01-01"
OG_TO_DATE = "2004-01-03"
from_date_obj = datetime.datetime.strptime(FROM_DATE, '%Y-%m-%d')
to_date_obj = datetime.datetime.strptime(TO_DATE, '%Y-%m-%d')
date_diff = to_date_obj - from_date_obj
SYMBOLS = []
SYMBOL_INDEX = 0
SYMBOL = None
NUM_PICS = 4000
APIKEY = "J6wnkSNzZpMvfBqBORVBxjMjhLrZQ7lX"
TIME_MULT = 1
TIME_INT = "hour"
CUR_DATE = datetime.datetime.now()

symbol_file = open("./symbols.txt")
for line in symbol_file:
    line = line.strip()
    SYMBOLS.append(line)

SYMBOL = SYMBOLS[SYMBOL_INDEX]
symbol_file.close()


def generate_urls():
    global FROM_DATE, TO_DATE, SYMBOL, to_date_obj, from_date_obj
    urls = []
    N = NUM_PICS
    symb_index = 0
    while N > 0 and symb_index - 1 < len(SYMBOLS):
        url = f"https://financialmodelingprep.com/api/v3/historical-chart/{TIME_MULT}{TIME_INT}/{SYMBOL}?from={FROM_DATE}&to={TO_DATE}&apikey={APIKEY}"
        urls.append(url)
        N -= 1
        from_date_obj += date_diff
        to_date_obj += date_diff
        FROM_DATE = from_date_obj.strftime('%Y-%m-%d')
        TO_DATE = to_date_obj.strftime('%Y-%m-%d')

        if (from_date_obj > CUR_DATE):
            symb_index += 1
            SYMBOL = SYMBOLS[symb_index]
            FROM_DATE = OG_FROM_DATE
            TO_DATE = OG_TO_DATE
            from_date_obj = datetime.datetime.strptime(OG_FROM_DATE, '%Y-%m-%d')
            to_date_obj = datetime.datetime.strptime(OG_TO_DATE, '%Y-%m-%d')
            continue
    
    return urls

            

urls = generate_urls()

#print(urls)

API_CALLS_PER_MIN = 300
NUM_API_CALLS = 0
json_datas = []


for url in urls:
    r = requests.get(url)
    NUM_API_CALLS += 1
    try:
        json_data = r.json()
        
        if json_data == []:
            continue
        else:
            json_datas.append(json_data)
        if (NUM_API_CALLS % API_CALLS_PER_MIN == 0):
            print("SLUMBER")
            print(json_datas)
            time.sleep(61)
  
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")




