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
while True:
    r = requests.get(url)
    json_data = r.json()
    i += 1
    print(json_data)
    print()
    break


