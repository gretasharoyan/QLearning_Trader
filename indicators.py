import colorsys
import datetime as dt  		  	   		  	  			  		 			     			  	 
import os  		  	   		  	  			  		 			     			  	   		  	   		  	  			  		 			     			  	 
import numpy as np  		  	   		  	  			  		 			     			  	   		  	   		  	  			  		 			     			  	 
import pandas as pd  		  	   		  	  			  		 			     			  	 
from util import get_data, plot_data  	
import matplotlib.pyplot as plt


def author(): 
  return 'gsharoyan3' 



#Equations from: https://school.stockcharts.com/doku.php?id=technical_indicators:moving_average_convergence_divergence_macd
def MACD(data):
      lookback = 12
      lookback_long = 26
      lookback_signal = 9

      ema = data.ewm(span = lookback, adjust=False, min_periods=lookback).mean()
      ema_long = data.ewm(span = lookback_long, adjust=False,  min_periods=lookback_long).mean()
      price_sma_ratio = data/ema
      macd = ema - ema_long
      signal = macd.ewm(span = lookback_signal, adjust=False, min_periods=lookback_signal).mean() 
      macd_hist = macd - signal
      
      return macd - signal


#Equations from: https://www.cmcmarkets.com/en/trading-guides/what-is-a-stochastic-indicator
def stochastic_indicator(data, symbol):
      k_period = 14
      d_period = 3
      
      
      high = data["High"].rolling(k_period).max()
      low = data["Low"].rolling(k_period).min()

      
      k = (data[symbol] - low)*100/(high - low)
      d = k.rolling(d_period).mean()     
      
      return k



def rsi(data):
      
      lookback = 20
      
      daily_rets = data.copy()
      daily_rets.values[1:,:] = data.values[1:,:] - data.values[:-1, :]
      daily_rets.values[0,:] = np.nan

      up_rets = daily_rets[daily_rets >=0].fillna(0).cumsum()
      down_rets = -1 * daily_rets[daily_rets < 0].fillna(0).cumsum()
      
      up_gain = data.copy()
      up_gain.ix[:,:] = 0
      up_gain.values[lookback:,:] = up_rets.values[lookback:,:] - up_rets.values[:-lookback, :]

      down_loss = data.copy()
      down_loss.ix[:,:] = 0
      down_loss.values[lookback:,:] = down_rets.values[lookback:,:] - down_rets.values[:-lookback, :]      


      rs = (up_gain / lookback) / (down_loss / lookback)
      

      rsi = 100 - (100/ (1 + rs))
      rsi.ix[:lookback, :] = np.nan
      
      rsi[rsi == np.inf] = 100
      
      return rsi
      
      

def sma(data):
      lookback = 20

      sma = data.rolling(window = lookback, min_periods = lookback).mean()
      price_sma_ratio = data/sma
            
      return price_sma_ratio
      
      
      
      
      
     
def bollinger(data):
      lookback = 20

      sma = data.rolling(window = lookback, min_periods = lookback).mean()
      rolling_std = data.rolling(window = lookback, min_periods = lookback).std()
      top_band = sma + (2*rolling_std)
      bottom_band = sma - (2*rolling_std)
      bbp = (data - bottom_band)/(top_band-bottom_band)

      return bbp
     

    
def momentum(data):
      lookback = 15
      mom = (data[lookback:] / data[:-lookback].values) - 1 

      return mom



def run(
  symbol='JPM',  		  	   		  	  			  		 			     			  	   
  sd = dt.datetime(2008, 1, 1),
	ed = dt.datetime(2009, 12, 31),	  
  sv =100000	   
):
  
    dates = pd.date_range(sd, ed)  		  	   		  	  			  		 			     			  	 
    prices_all = get_data([symbol], dates, addSPY = False)
    prices_all_high = get_data([symbol], dates, addSPY = False, colname = "High")
    prices_all_high.rename(columns={symbol: "High",}, inplace = True)
    prices_all_low = get_data([symbol], dates, addSPY = False, colname = "Low")
    prices_all_low.rename(columns={symbol: "Low"}, inplace= True)
    prices_all_close = get_data([symbol], dates, addSPY = False, colname = "Close")
    
    prices_all.dropna(inplace=True)
    result = prices_all_high.join(prices_all_low)
    result.dropna(inplace=True)
    result = result.join(prices_all_close)
  
    bollinger(prices_all)
    momentum(prices_all)
    sma(prices_all)
    rsi(prices_all)
    stochastic_indicator(result)
    MACD(prices_all)

  