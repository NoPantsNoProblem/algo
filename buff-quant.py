!# /bin/env python3


import datetime as dt
import pandas as pd
import concurrent.futures as cf
from yahoofinancials import YahooFinancials
import re
from ast import literal_eval
import time
import requests
from bs4 import BeautifulSoup

import numpy as N




# get data from yahoo finance.

#list_inp = [100, 75, 100, 20, 75, 12, 75, 25]
stocks = ["GOOGL", "APPL", "PFE"]

# numpy way
na = N.array(stocks)
unqStock = N.unique(na)
print("Stock {}".format(unqStock))


# ---------------------------------------------------------------------

asx_200 = 'https://www.asx200list.com/'
all_ords = 'https://www.allordslist.com/'
small_ords = 'https://www.smallordslist.com/'
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
}
ASX200, ALLORDS, SMALLORDS = [], [], []
asx_list = [ASX200, ALLORDS, SMALLORDS]
for index, url in enumerate([asx_200, all_ords, small_ords]):
    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')
    divs = soup.findAll(
        'table', class_='tableizer-table sortable')[0].findAll('tbody')
    for i, val in enumerate(divs[0]):
        if len(val) > 1:
            text = re.sub(r"[<trd>]", "", str(val))
            text = text.split('/')
            asx_list[index].append(text[0])

print('ASX200', ASX200)
print('SMALLORDS', SMALLORDS)
print('ALLORDS', ALLORDS)

# -------------------------------------------------------------------

stockList = ASX200
stocks = [stock + '.AX' for stock in stockList]
stocks_set = set(stocks)
contains_duplicates = len(stocks_set) != len(stocks)
contains_duplicates = any(stocks.count(stock) > 1 for stock in stockList)
print(len(stocks_set), len(stocks), contains_duplicates)

# ---------------------------------------------------------------------


balanceSheet = {}
incomeStatement = {}
cashStatement = {}


def retrieve_stock_data(stock):
    try:
        print(stock)
        yahoo_financials = YahooFinancials(stock)
        balance_sheet_data = yahoo_financials.get_financial_stmts(
            'annual', 'balance')
        income_statement_data = yahoo_financials.get_financial_stmts(
            'annual', 'income')
        cash_statement_data = yahoo_financials.get_financial_stmts(
            'annual', 'cash')
        balanceSheet[stock] = balance_sheet_data['balanceSheetHistory'][stock]
        incomeStatement[stock] = income_statement_data['incomeStatementHistory'][stock]
        cashStatement[stock] = cash_statement_data['cashflowStatementHistory'][stock]
    except:
        print('error with retrieving stock data')

        with open('balanceSheet_ASX200.txt', 'w') as output:
    output.write(str(balanceSheet))


with open('incomeStatement_ASX200.txt', 'w') as output:
    output.write(str(incomeStatement))
with open('cashStatement_ASX200.txt', 'w') as output:
    output.write(str(cashStatement))


start = time.time()
executor = cf.ThreadPoolExecutor(16)
futures = [executor.submit(retrieve_stock_data, stock) for stock in stocks]
cf.wait(futures)
end = time.time()
print('  time taken {:.2f} s'.format(end-start))
