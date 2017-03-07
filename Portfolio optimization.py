# -*- coding: utf-8 -*-
"""
Created on Mon Feb 06 09:05:10 2017

@author: jens_
"""

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from itertools import product


dt_start = dt.datetime(2010, 1, 1)
dt_end = dt.datetime(2010, 12, 31)
allocation = [0.0, 0.0, 0.0, 1.0]
Symbols =    ['C', 'GS', 'IBM', 'HNZ']


dt_timeofday = dt.timedelta(hours=16)
ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
c_dataobj = da.DataAccess('Yahoo')
ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
ldf_data = c_dataobj.get_data(ldt_timestamps, Symbols, ls_keys)
d_data = dict(zip(ls_keys, ldf_data))
actual_closes = d_data["close"].values


def simulate(startdate, enddate, symbols, allocation):
    cumulative_returns = []
    portfolio_daily_returns = []
    for i in range(1,len(actual_closes)):
        cumulative_returns.append(actual_closes[i]/actual_closes[0])
        
    cumulative_returns = np.array(cumulative_returns)
    portfolio_value = allocation * cumulative_returns
    portfolio_daily_value = np.sum(portfolio_value, axis=1)
    portfolio_daily_returns = []
    
    for i in range(1,len(portfolio_daily_value)):
        portfolio_daily_returns.append(portfolio_daily_value[i]/portfolio_daily_value[i-1]-1)
    
    portfolio_average_daily_return = np.mean(portfolio_daily_returns)
    std_dev_portfolio = np.std(portfolio_daily_returns)
    sharpe_portfolio = np.sqrt(len(portfolio_value))*portfolio_average_daily_return / std_dev_portfolio
    Start Date: , startdate
    "End Date:" , enddate
    "Symbols:", symbols
    "Optimal Allocations: ", allocation
    "Sharpe Ratio: ", sharpe_portfolio
    "Volatility (stdev of daily returns): ", std_dev_portfolio
    "Average Daily Return: ", portfolio_average_daily_return
    "Cumulative Return: ", portfolio_daily_value[-1]
    return sharpe_portfolio

#create all possible portfolio allocations

elements = [x/10. for x in range(11)]
combos = list(product(elements, repeat = 4))
combos = [x for x in combos if sum(x) == 1]
          
#example for finding the portfolio with the highest sharpe ratio

sharpes = []

for i in combos: 
    sharpes.append(simulate(dt_start, dt_end, Symbols, i))
 
#locate the allocation with the highest sharpe ratio    
print combos[sharpes.index(max(sharpes))]
       




