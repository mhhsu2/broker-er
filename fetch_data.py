import os
import time
from datetime import date
import argparse
from tqdm import tqdm

import numpy as np
import pandas as pd

import yfinance as yf
from get_all_tickers import get_tickers
import requests


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = 'data'
NUM_COMPANY = 500
STOCK_DATA_LENGTH = '2y'

def get_stock_data(num_company, length):

    # Get a list of top N US stock tickers
    print(f"Start fetching top {NUM_COMPANY} stock tickers")
    list_top_n_tickers = get_tickers.get_biggest_n_tickers(NUM_COMPANY)
    print(f"Finished")

    # Get stock history data
    print(f"Start downloading top {NUM_COMPANY} stock data with length {STOCK_DATA_LENGTH}")
    data = pd.DataFrame()
    pbar = tqdm(range(len(list_top_n_tickers)))
    for tick in list_top_n_tickers:

        # Get individual stock data from yahoo finance API
        stock_data = yf.Ticker(tick)
        df = stock_data.history(period=STOCK_DATA_LENGTH)

        # Add stock symbol (ticker) 
        df.insert(0, 'Ticker', tick)

        # Concat data
        data = pd.concat([df, data]) 
        
        pbar.update(1)
        time.sleep(1) # Avoid getting banned from yahoo finance

    pbar.close()

    # Save data in to .csv
    data = data.reset_index()
    file_name = f'top{NUM_COMPANY}_{STOCK_DATA_LENGTH}_{date.today().strftime("%b-%d-%Y")}_stock_data.csv'
    save_path = os.path.join(ROOT_DIR, DATA_DIR, file_name)
    data.to_csv(save_path, index=False, header=True)
    print(f"Data file located at {save_path}")

if __name__ == "__main__":
    get_stock_data(NUM_COMPANY, STOCK_DATA_LENGTH)








