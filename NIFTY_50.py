from nsepy import get_history
import bs4 as bs
import pickle
import requests
import pandas as pd
import datetime as dt
import os
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
style.use('ggplot')
pd.core.common.is_list_like = pd.api.types.is_list_like

#FUNCTION TO SAVE TICKERS

def save_SP():
    tickers = []
    resp = requests.get('https://en.wikipedia.org/wiki/NIFTY_50')
    soup = bs.BeautifulSoup(resp.text,'lxml')
    table = soup.find('table',{'id':'constituents'})
    
    for row in table.find_all('tr')[1:]:
        ticker = row.find_all('td')[1].text.replace('\n','')
        if "." in ticker:
            ticker = ticker.replace('.NS','')
            print('ticker replaced to', ticker) 
        tickers.append(ticker)
        
        with open("NIFTYticker.pickle","wb") as f:
            pickle.dump(tickers,f)
    return tickers    
 
tickers = save_SP()

#FUNCTION TO DOWNLOAD STOCK DATA

def get_data_NIFTY(reload_sp500 = False):
    if reload_sp500:
        tickers = save_SP()
        
    else:
        with open("NIFTYticker.pickle","rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs_NIFTY'):
        os.makedirs('stock_dfs_NIFTY')
    start_date = dt.datetime(2000,1,1)
    end_date = dt.datetime(2020,12,31)
   
    for ticker in tickers:
        if not os.path.exists('stock_dfs_NIFTY/{}.csv'.format(ticker)):
            df = get_history(ticker, start=start_date, end=end_date)
            df.to_csv('stock_dfs_NIFTY/{}.csv'.format(ticker))
        else:
            print('Already Have {}'.format(ticker))
            
get_data_NIFTY()
