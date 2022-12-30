#! /bin/env python3

# pip install yfinance and pandas if they are not installed

import yfinance as yf
import pandas as pd
import shutil, os, time, glob, smtplib, ssl
from get_all_tickers import get_tickers as gt

# List of the stocks we are interested in analyzing. At the time of writing this, it narrows the list of stocks down to 44. If you have a list of your own you would like to use just create a new list instead of using this, for example: tickers = ["FB", "AMZN", ...] 
tickers = gt.get_tickers_filtered(mktcap_min=150000, mktcap_max=10000000)
# Check that the amount of tickers isn't more than 1800
print("The amount of stocks chosen to observe: " + str(len(tickers)))

# These two lines remove the Stocks folder and then recreate it in order to remove old stocks.
shutil.rmtree("<Your Path>\\Daily_Stock_Report\\Stocks\\")
os.mkdir("<Your Path>\\Daily_Stock_Report\\Stocks\\")
# Holds the amount of API calls we executed
Amount_of_API_Calls = 0
# This while loop is reponsible for storing the historical data for each ticker in our list. Note that yahoo finance sometimes incurs json.decode errors and because of this we are sleeping for 2 seconds after each iteration, also if a call fails we are going to try to execute it again. Also, do not make more than 2,000 calls per hour or 48,000 calls per day or Yahoo Finance may block your IP. The clause "(Amount_of_API_Calls < 1800)" below will stop the loop from making too many calls to the yfinance API.Prepare for this loop to take some time. It is pausing for 2 seconds after importing each stock.
Stock_Failure = 0  # Used to make sure we don't waste too many API calls on one Stock ticker that could be having issues
Stocks_Not_Imported = 0
# Used to iterate through our list of tickers
i=0
while (i < len(tickers)) and (Amount_of_API_Calls < 1800):
    try:
        stock = tickers[i]  # Gets the current stock ticker
        temp = yf.Ticker(str(stock))
        Hist_data = temp.history(period="max")  # Tells yfinance what kind of data we want about this stock (In this example, all of the historical data)
        Hist_data.to_csv("<Your Path>\\Daily_Stock_Report\\Stocks\\"+stock+".csv")  # Saves the historical data in csv format for further processing later
        time.sleep(2)  # Pauses the loop for two seconds so we don't cause issues with Yahoo Finance's backend operations
        Amount_of_API_Calls += 1 
        Stock_Failure = 0
        i += 1  # Iteration to the next ticker
    except ValueError:
        print("Yahoo Finance Backend Error, Attempting to Fix")  # An error occured on Yahoo Finance's backend. We will attempt to retreive the data again
        if Stock_Failure > 5:  # Move on to the next ticker if the current ticker fails more than 5 times
            i+=1
            Stocks_Not_Imported += 1
        Amount_of_API_Calls += 1
        Stock_Failure += 1
print("The amount of stocks we successfully imported: " + str(i - Stocks_Not_Imported))