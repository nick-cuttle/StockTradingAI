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

#matplotlib.use('agg')
#CONSTANTS
MAX_REQ_ERR = "You've exceeded the maximum requests per minute"
RED = '\033[91m'
RESET = '\033[0m'  # Reset color to default
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'

#Class to represent a candle
class Candle():

    def __init__(self, open, close, hi, low, vol, time, date):
        self.open = open
        self.close = close
        self.high = hi
        self.low = low
        self.vol = vol
        self.time = time
        self.date = date

    def __repr__(self):
        return f"(o:{self.open}, c:{self.close}, h:{self.high}, l:{self.low}, v:{self.vol}, t:{self.time}, d:{self.date})"

def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Data Collection Arguments.')

    # Add a command-line flag
    parser.add_argument('-s', '--symbol', required=True, type=str, help = 'Company Symbol')
    parser.add_argument('-fd', '--from-date', required=True, type=str, help = 'From Date')
    parser.add_argument('-td', '--to-date', required=True, type=str, help = 'To Date')
    parser.add_argument('-ti', '--time-int', required=True, type=str, help = "Time Interval")
    parser.add_argument('-tm', '--time-mult', required=True, type=int, help = "Time Multiplier")
    parser.add_argument('-n', '--num-pics', default=1, type=int, help = "Number of pictures to take (default: 1)")

    # Parse the command-line arguments
    args = parser.parse_args()

    TIME_INT = args.time_int
    TIME_MULT = args.time_mult
    SYMBOL = args.symbol.upper()
    OG_FROM_DATE = args.from_date
    OG_TO_DATE = args.to_date
    FROM_DATE = args.from_date
    TO_DATE = args.to_date
    NUM_PICS = args.num_pics
    CAM = Camera()

    #Detect if we need to parse all symbols in list
    SYMBOLS = []
    SYMBOL_INDEX = 0
    if SYMBOL == "ALL":
        symbol_file = open("./symbols.txt")
        for line in symbol_file:
            line = line.strip()
            SYMBOLS.append(line)

        #NUM_PICS = 9999999999
        SYMBOL = SYMBOLS[SYMBOL_INDEX]
        symbol_file.close()

    #Get the difference in the time range.
    from_date_obj = datetime.datetime.strptime(FROM_DATE, '%Y-%m-%d')
    to_date_obj = datetime.datetime.strptime(TO_DATE, '%Y-%m-%d')
    date_diff = to_date_obj - from_date_obj
    APIKEY = "J6wnkSNzZpMvfBqBORVBxjMjhLrZQ7lX"
    IMG_DIR = "./test_imgs/"
    LIMIT = 50000
    CUR_DATE = datetime.datetime.now()

    matplotlib.use('Agg')
    #Continuously loop while we still have pics to take or all symbols aren't done.
    while NUM_PICS > 0 and (SYMBOL_INDEX <= len(SYMBOLS) - 1):

        url = f"https://financialmodelingprep.com/api/v3/historical-chart/{TIME_MULT}{TIME_INT}/{SYMBOL}?from={FROM_DATE}&to={TO_DATE}&apikey={APIKEY}"

        r = requests.get(url)
        json_data = r.json()

        if (from_date_obj > CUR_DATE):
            SYMBOL_INDEX += 1
            SYMBOL = SYMBOLS[SYMBOL_INDEX]
            FROM_DATE = OG_FROM_DATE
            TO_DATE = OG_TO_DATE
            from_date_obj = datetime.datetime.strptime(OG_FROM_DATE, '%Y-%m-%d')
            to_date_obj = datetime.datetime.strptime(OG_TO_DATE, '%Y-%m-%d')
            print(f"{BLUE}!     CHANGING TO NEXT SYMBOL: {SYMBOL}       !      {RESET}")
            continue

        if json_data == []:
            from_date_obj += date_diff
            to_date_obj += date_diff
            FROM_DATE = from_date_obj.strftime('%Y-%m-%d')
            TO_DATE = to_date_obj.strftime('%Y-%m-%d')
            continue
        
        #get all candles.
        chart = []
        for candle_json in json_data:

            # Convert the timestamp to a datetime object
            # dt_object = datetime.datetime.strptime(candle_json["date"], '%Y-%m-%d %H:%M:%S')

            # Format the datetime object as YYYY-MM-DD
            formatted_date = candle_json["date"]

            op = float(candle_json["open"])
            hi = float(candle_json["high"])
            low = float(candle_json["low"])
            cl = float(candle_json["close"])
            vol = float(candle_json["volume"])

            candle = Candle(op, cl, hi, low, vol, formatted_date, formatted_date)
            chart.append(candle)

        #sort candles and collect in dictionary for matplotlib.
        chart = sorted(chart, key=lambda x: x.time)
        data = {
            'Open': [],
            'High': [],
            'Low': [],
            'Close': [],
            'Volume': []
        }

        sorted_candles = chart

        #get first and last candles.
        direction = None
        first_candle = sorted_candles[0]
        last_candle = sorted_candles[len(sorted_candles) - 1]

        #calculate slope between first and last candle for direction.
        tolerance = 0.09
        fc_date_obj = datetime.datetime.strptime(first_candle.date, '%Y-%m-%d %H:%M:%S')
        lc_date_obj = datetime.datetime.strptime(last_candle.date, '%Y-%m-%d %H:%M:%S')
        time_difference = fc_date_obj - lc_date_obj
        dx = time_difference.total_seconds() * (1/86_400)
        dy = last_candle.close - first_candle.close 
        slope = 0
        if (dx != 0):
            slope = -1 * (dy / dx)

        #Set the direction of the chart.
        if slope > 0 and slope > tolerance:
            direction = "UP"
        elif slope < 0 and abs(slope) > tolerance:
            direction = "DOWN"
        else:
            direction = "NEUTRAL"

        #print(f"{YELLOW} SLOPE: {slope}, DIRECTION: {direction}{RESET}")

        #fill data for matplotlib
        times = []
        for candle in sorted_candles:
            # convert into datetime object
            data['Open'].append(candle.open)
            data['High'].append(candle.high)
            data['Low'].append(candle.low)
            data['Close'].append(candle.close)
            data['Volume'].append(candle.vol)
            times.append(candle.time)

        #create a panda dataframe to store data with times.
        df = pd.DataFrame(data, index=pd.to_datetime(times))

        fname = IMG_DIR + direction + str(CAM.count_files(dir="./test_imgs") + 1) + ".png"

        save = dict(fname= fname, pad_inches=0, bbox_inches='tight')
        # Plot candles using mplfinance
        #, figsize=(20, 10)
        fig, axlist = plot(df, type='candle', style='yahoo', returnfig=True, volume=False)
        ax = axlist[0]
        #Hide x and y axes
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        fig.savefig(fname, bbox_inches='tight', pad_inches=0)
        plt.close(fig)
        del fig
        gc.collect()
    

        #create all labels for this graph.
        labels = [f"DIRECTION: {direction}", f"TIME_INT: {TIME_MULT}_{TIME_INT}", f"SYMBOL: {SYMBOL}", f"FROM_DATE: {FROM_DATE}", f"TO_DATE: {TO_DATE}"]

        #create the label and .png file, and close figure.
        CAM.create_label_file(labels, dir="./test_labels/")
        #fig.savefig(fname, bbox_inches='tight', pad_inches=0)
        #plt.close(fig, clear=True)
        # gc.collect()
        # time.sleep(0.1)

        NUM_PICS -= 1
        print(f"{GREEN}'{fname}' was created from dates: {FROM_DATE}-{TO_DATE}{RESET}")

        #update date to next.
        from_date_obj += date_diff
        to_date_obj += date_diff
        FROM_DATE = from_date_obj.strftime('%Y-%m-%d')
        TO_DATE = to_date_obj.strftime('%Y-%m-%d')

if __name__ == "__main__":
    print(f"{GREEN}||================================================||{RESET}")
    print(f"{GREEN}         API STARTED SUCCESSFULLY{RESET}")
    print(f"{GREEN}||================================================||{RESET}")
    print()
    main()
    print()
    print(f"{GREEN}||================================================||{RESET}")
    print(f"{GREEN}         API TERMINATED SUCCESSFULLY{RESET}")
    print(f"{GREEN}||================================================||{RESET}")
    







