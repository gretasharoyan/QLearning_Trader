 	   		  	  			  		 			     			  	 
import datetime as dt  		  	   		  	  			  		 			     			  	 
import random  		 
import numpy as np 	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
import pandas as pd  		  	   		  	  			  		 			     			  	 
import util as ut  
from util import get_data 		  	   		  	  			  		 			     			  	 
  		  	   		
from marketsimcode import compute_portvals    
import indicators	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
class ManualStrategy(object):  		  	   		  	  			  		 			     			  	 	  	   		  	  			  		 			     			  	 
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		  	  			  		 			     			  	 
        """  		  	   		  	  			  		 			     			  	 
        Constructor method  		  	   		  	  			  		 			     			  	 
        """  		  	   		  	  			  		 			     			  	 
        self.verbose = verbose  		  	   		  	  			  		 			     			  	 
        self.impact = impact  		  	   		  	  			  		 			     			  	 
        self.commission = commission  
        self.start_val = 100000		  
        self.symbol = "JPM"	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
  	   		  	  			  		 			     			  	 
    def plot(self, df_trades, title):
        compute_portvals(df_trades, symbol = self.symbol, start_val=self.start_val, commission=self.commission, impact=self.impact, title = title, verbose = self.verbose)  
        	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    # this method should use the existing policy and test it against new data  		  	   		  	  			  		 			     			  	 
    def testPolicy(  		  	   		  	  			  		 			     			  	 
        self,  		  	   		  	  			  		 			     			  	 
        symbol="JPM",  		  	   		  	  			  		 			     			  	 
        sd=dt.datetime(2008, 1, 1),  		  	   		  	  			  		 			     			  	 
        ed=dt.datetime(2009, 12, 31),  		  	   		  	  			  		 			     			  	 
        sv=100000,  		  	   		  	  			  		 			     			  	 
    ):  		  	   		  	  			  		 			     			  	 			  		 			     			  	 
        pd.set_option('display.float_format', lambda x: '%.2f' % x)
        self.start_val = sv
        self.symbol = symbol

        order = [symbol]
        lookback_max = 60
        dates = pd.date_range(sd - dt.timedelta(days = lookback_max), ed)  		  	   		  	  			  		 			     			  	 
        prices_all = get_data(order, dates) 
        prices_all.drop(columns=['SPY'], inplace = True) 		  	   		  	  			  		 			     			  	 

 		  	   		  	  			  		 			     			  	 
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
        

        i_bollinger = indicators.bollinger(prices_all)
        i_momentum = indicators.momentum(prices_all)
        i_sma = indicators.sma(prices_all)
        i_rsi = indicators.rsi(prices_all)
        i_stochastic = indicators.stochastic_indicator(result, self.symbol)
        i_MACD = indicators.MACD(prices_all)

        i_rsi = i_rsi.rename(columns = {self.symbol: "RSI"})
        i_momentum = i_momentum.rename(columns = {self.symbol: "Momentum"})
        i_bollinger = i_bollinger.rename(columns = {self.symbol: "Bollinger"})
        i_sma = i_sma.rename(columns = {self.symbol: "SMA"})

        i_stochastic.name = "Stoch_K"
        i_stochastic = i_stochastic.to_frame()

        i_MACD = i_MACD.rename(columns = {self.symbol: "MACD"})     
        all_indicators = i_rsi.join([i_bollinger, i_stochastic, i_momentum, i_MACD, i_sma])

        all_indicators["Stoch_D"] = all_indicators['Stoch_K'].rolling(3).mean()
        all_indicators["Stoch_Diff"] = all_indicators['Stoch_K'] - all_indicators['Stoch_D']
              
        start = all_indicators.index.searchsorted(sd)

        
        all_indicators = all_indicators[start:]

        all_indicators.reset_index(level = 0, inplace = True)

        
        rsi_buy = False
        rsi_sell = False
    
        
        bb_buy = False
        bb_sell = False
        
        mom_buy = False
        mom_sell = False
        
        MACD_buy = False
        MACD_sell = False

        all_indicators['Total_Stock'] = 0.0
        all_indicators['Trades'] = 0.0

        all_indicators['Total'] = 0.0


        for i in all_indicators.index[1:-1]:
            stoch_df = all_indicators.loc[i, "Stoch_Diff"]
            stoch_k = all_indicators.loc[i, "Stoch_K"]
            stoch_d = all_indicators.loc[i, "Stoch_D"] 
            MACD_i = all_indicators.loc[i, "MACD"] 
            rsi_i = all_indicators.loc[i, "RSI"] 
            bb_i = all_indicators.loc[i, "Bollinger"] 
            sma_i = all_indicators.loc[i, "SMA"] 
            mom_i = all_indicators.loc[i, "Momentum"] 

            all_indicators.at[i,'Total_Stock'] = all_indicators.loc[i-1, 'Total_Stock']   
                
            if rsi_i < 40:
                rsi_buy = True
                rsi_sell = False

            elif rsi_i > 60:
                rsi_buy = False
                rsi_sell = True 
            else:
                rsi_buy = False
                rsi_sell = False
                
                
            if MACD_i > 0:
                MACD_buy = True
                MACD_sell = False

            elif MACD_i < 0:
                MACD_buy = False
                MACD_sell = True 
            else:
                MACD_buy = False
                MACD_sell = False
                
            if bb_i >1:
                bb_sell = True
                bb_buy = False
            elif bb_i<0:
                bb_buy = True 
                bb_sell = False
            else:
                bb_sell = False
                bb_buy = False
                
            if mom_i >.1:
                mom_sell = True
                mom_buy = False
            elif mom_i<-.1:
                mom_buy = True 
                mom_sell = False
            else:
                mom_sell = False
                mom_buy = False               
                       
                
            if mom_buy and  bb_buy and rsi_buy:
            # if MACD_buy:
                sma_buy = False
                bb_buy = False
                mom_buy = False

                if all_indicators.loc[i-1, 'Total_Stock'] == -1000:
                    all_indicators.at[i,'Total_Stock'] = all_indicators.loc[i-1, 'Total_Stock'] + 2000 
                    all_indicators.at[i,'Trades'] = 2000        
                elif  all_indicators.loc[i-1, 'Total_Stock'] == 0:           
                    all_indicators.at[i,'Total_Stock'] = all_indicators.loc[i-1, 'Total_Stock'] + 1000 
                    all_indicators.at[i,'Trades'] = 1000                  
                
                
            if mom_sell and bb_sell or rsi_sell:
            # if MACD_sell:
                sma_sell = False
                bb_sell = False
                mom_sell = False
         
                if all_indicators.loc[i-1, 'Total_Stock'] == 1000:
                    all_indicators.at[i,'Total_Stock'] = all_indicators.loc[i-1, 'Total_Stock'] - 2000 
                    all_indicators.at[i,'Trades'] = -2000        
                elif  all_indicators.loc[i-1, 'Total_Stock'] == 0:           
                    all_indicators.at[i,'Total_Stock'] = all_indicators.loc[i-1, 'Total_Stock'] - 1000 
                    all_indicators.at[i,'Trades'] = -1000                   
        
        
        all_indicators.set_index("index", inplace=True)	
        df_trades = all_indicators.copy()

        df_trades.drop(columns = ["RSI", "MACD", "Stoch_K", "Stoch_D", "Stoch_Diff", "Total_Stock", "Total", "SMA", "Momentum", "Bollinger"], inplace=True)  

        return df_trades
    

         	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
if __name__ == "__main__":  		  	   		  	  			  		 			     			  	 	
    
    sym = "JPM"
    comm = 9.95
    imp = 0.005
    start_in = dt.datetime(2008, 1, 1)
    end_in = dt.datetime(2009, 12, 31)
    start_out = dt.datetime(2010, 1, 1)
    end_out = dt.datetime(2011, 12, 31)
    start_val = 100000
    	  	   		  	  			  		 			     			  	 
    manual = ManualStrategy(verbose=False, impact=imp, commission=comm)  	   		  	  			  		 			     			  	 
    df_trades = manual.testPolicy(symbol='JPM', sd = start_in, ed=end_in, sv = start_val)  
    manual.plot(df_trades, "In-Sample Manual vs Benchmark for " + sym)
    
    df_trades = manual.testPolicy(symbol='JPM', sd = start_out, ed=end_out, sv = start_val)  
    manual.plot(df_trades, "Out-of-Sample Manual vs Benchmark for " + sym)
    
