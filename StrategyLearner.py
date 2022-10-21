  	   		  	  			  		 			     			  	 
import datetime as dt  		  	   		  	  			  		 			     			  	 
import random  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
import pandas as pd  		  	   		  	  			  		 			     			  	 
import util as ut  
from util import get_data

# from marketsimcode import compute_portvals    
import indicators		
import numpy as np	  	
import QLearner as ql  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
class StrategyLearner(object):  		  	   		  	  			  		 			     			  	 
	  	   		  	  			  		 			     			  	 
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		  	  			  		 			     			  	 
        """  		  	   		  	  			  		 			     			  	 
        Constructor method  		  	   		  	  			  		 			     			  	 
        """  		  	   		  	  			  		 			     			  	 
        self.verbose = verbose  		  	   		  	  			  		 			     			  	 
        self.impact = impact  		  	   		  	  			  		 			     			  	 
        self.commission = commission  	
        self.steps = 7
        
        self.rsi_steps = 8
        self.bb_steps = 6
        self.mom_steps = 6
        
        self.threshold_rsi = np.zeros(self.rsi_steps)
        self.threshold_bollinger = np.zeros(self.bb_steps)
        self.threshold_mom = np.zeros(self.mom_steps)
        

        self.learner = ql.QLearner(  		  	   		  	  			  		 			     			  	 
        num_states= 1000,  		  	   		  	  			  		 			     			  	 
        num_actions=3,  		  	   		  	  			  		 			     			  	 
        alpha=0.2,  		  	   		  	  			  		 			     			  	 
        gamma=.8,  		  	   		  	  			  		 			     			  	 
        rar=0.0,  		  	   		  	  			  		 			     			  	 
        radr=0.0,  		  	   		  	  			  		 			     			  	 
        dyna=0,  		  	   		  	  			  		 			     			  	 
        verbose=False,  		  	   		  	  			  		 			     			  	 
    ) 
        
    def discretize(self, rsi, bb, mom):  		  	   		  	  			  		 			     			  	         
        rsi_discrete = 0
        bb_discrete = 0
        mom_discrete = 0
        for i in range(self.rsi_steps):
            if i == 0:
                if rsi <= self.threshold_rsi[0]:
                    rsi_discrete = 0

            else:
                if rsi <= self.threshold_rsi[i] and rsi > self.threshold_rsi[i-1]:
                    rsi_discrete = i
   
        for i in range(self.bb_steps):
            if i == 0:
                if bb <= self.threshold_bollinger[0]:
                    bb_discrete = 0

            else:
                if bb <= self.threshold_bollinger[i] and bb > self.threshold_bollinger[i-1]:
                    bb_discrete = i             
        	  	
                       		
        for i in range(self.mom_steps):
            if i == 0:
                if mom <= self.threshold_mom[0]:
                    mom_discrete = 0

            else:
                if mom <= self.threshold_mom[i] and mom > self.threshold_mom[i-1]:
                    mom_discrete = i             
        	  	  	  			  		 			     			  	 
        return 	100*rsi_discrete + 10*bb_discrete + mom_discrete	  	   		  	  			  		 			     			  	 
  		  	   		  	  			  	  	   		  	  			
                                       	  	     		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    # this method trains QLearner 		  	   		  	  			  		 			     			  	 
    def add_evidence(  		  	   		  	  			  		 			     			  	 
        self,  		  	   		  	  			  		 			     			  	 
        symbol="IBM",  		  	   		  	  			  		 			     			  	 
        sd=dt.datetime(2008, 1, 1),  		  	   		  	  			  		 			     			  	 
        ed=dt.datetime(2009, 1, 1),  		  	   		  	  			  		 			     			  	 
        sv=10000,  		  	   		  	  			  		 			     			  	 
    ):  		  	   		  	  			  		 			     			  	 
        """  		  	   		  	  			  		 			     			  	 
        Trains your strategy learner over a given time frame.  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
        :param symbol: The stock symbol to train on  		  	   		  	  			  		 			     			  	 
        :type symbol: str  		  	   		  	  			  		 			     			  	 
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  	  			  		 			     			  	 
        :type sd: datetime  		  	   		  	  			  		 			     			  	 
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  	  			  		 			     			  	 
        :type ed: datetime  		  	   		  	  			  		 			     			  	 
        :param sv: The starting value of the portfolio  		  	   		  	  			  		 			     			  	 
        :type sv: int  		  	   		  	  			  		 			     			  	 
        """  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  				        
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
        

        
        
        i_bollinger = indicators.bollinger(prices_all)
        i_momentum = indicators.momentum(prices_all)
    
        i_rsi = indicators.rsi(prices_all)


        i_rsi = i_rsi.rename(columns = {symbol: "RSI"})
        i_momentum = i_momentum.rename(columns = {symbol: "Momentum"})
        i_bollinger = i_bollinger.rename(columns = {symbol: "Bollinger"})

        prices_all.dropna(inplace=True)
 
        all_2 = i_rsi.join([i_bollinger, i_momentum, prices_all])

        start = all_2.index.searchsorted(sd)


        all_2 = all_2[start:]
        
        start_rsi = i_rsi.index.searchsorted(sd) 
        start_bollinger = i_bollinger.index.searchsorted(sd) 
        start_mom = i_momentum.index.searchsorted(sd)        


        i_rsi = i_rsi[start_rsi:]
        i_bollinger = i_bollinger[start_bollinger:]
        i_momentum = i_momentum[start_mom:]



        all_2.reset_index(level = 0, inplace = True)	
        

        
        i_rsi = i_rsi.sort_values(by=['RSI'])
        i_bollinger = i_bollinger.sort_values(by=['Bollinger'])
        i_momentum = i_momentum.sort_values(by=['Momentum'])


        i_rsi.reset_index(level = 0, inplace = True)
        i_bollinger.reset_index(level = 0, inplace = True)
        i_momentum.reset_index(level = 0, inplace = True)

        #Get thresholds to discretize states
        
        stepsize_rsi = all_2.shape[0]/self.rsi_steps
        stepsize_bb = all_2.shape[0]/self.bb_steps
        stepsize_mom = all_2.shape[0]/self.mom_steps

        
        for i in range(self.rsi_steps):
    
            self.threshold_rsi[i] = i_rsi.loc[int((i+1)*stepsize_rsi) - 1, "RSI"]

        for i in range(self.bb_steps):
        
            self.threshold_bollinger[i] = i_bollinger.loc[int((i+1)*stepsize_bb) - 1, "Bollinger"]
            
        for i in range(self.mom_steps):
            
            self.threshold_mom[i] = i_momentum.loc[int((i+1)*stepsize_mom) - 1, "Momentum"]
            
        all_2["Cash"] = 0.0
        all_2["Trades"] = 0
        all_2["Holdings"] = 0
        all_2["Portfolio_Value"] = 0.0
        all_2["Daily Rets"] = 0.0
        all_2["Daily Prices"] = all_2[symbol]/all_2[symbol].shift(1) - 1
        daily_rets = all_2[symbol]/all_2[symbol].shift(1) - 1
        # print(daily_rets)
       
        all_2.at[0, "Cash"] = float(sv)

        r = 0

        for epoch in range(100):
            data = all_2.copy()
            
            
            first_rsi = data.loc[0, "RSI"]
            first_bb = data.loc[0, "Bollinger"]
            first_mom = data.loc[0, "Momentum"]
        
            state = self.discretize(first_rsi, first_bb, first_mom)  # convert the location to a state  		  	   		  	  			  		 			     			  	 
            action = self.learner.querysetstate(state) 
                            
            for i in data.index:		   
                rsi = data.loc[i, "RSI"]
                bb = data.loc[i, "Bollinger"]
                mom = data.loc[i, "Momentum"]
                state = self.discretize(rsi, bb, mom)
                # print(state)
                price =  data.loc[i, symbol]
                if i != data.shape[0]-1:
                    tomorrow_price =  data.loc[i+1, symbol]
                else:
                    tomorrow_price = price
                #Do nothing
                if action == 2 and i == 0:
                    if i == 0:
                        data.at[i, 'Portfolio_Value'] = data.loc[i, 'Cash']
                        r = data.loc[i, 'Daily Rets']
                        # r = 0
                        r = 0
                    
                if i!=0:
                        
                    data.at[i, 'Cash'] = data.loc[i-1, 'Cash']  
                    data.at[i, 'Trades'] = 0
                    data.at[i, 'Holdings'] = data.loc[i-1, 'Holdings']
                    data.at[i, 'Portfolio_Value'] = data.loc[i, 'Cash'] + data.loc[i, symbol]*data.loc[i, 'Holdings']
                    data.at[i, 'Daily Rets'] = data.loc[i, 'Portfolio_Value']/data.loc[i-1, 'Portfolio_Value'] - 1
                    r = 0
                #Long
                if action == 1:
                    price = (1+self.impact)*price
                    if i == 0:
                        data.at[i, 'Trades'] = 1000
                        data.at[i, 'Holdings'] = 1000
                        data.at[i, 'Cash'] = data.loc[i, 'Cash'] - float((1000 * price*(1+self.impact))) - self.commission
                        data.at[i, 'Portfolio_Value'] = data.loc[i, 'Cash'] + price*data.loc[i, 'Holdings']
                        # r = data.loc[i, 'Daily Rets']
                        
                    else:
                        if data.loc[i-1, 'Holdings'] == -1000:
                            data.at[i, 'Trades'] = 2000
                            data.at[i, 'Cash'] = data.loc[i-1, 'Cash'] - float((data.loc[i, 'Trades'] * price*(1+self.impact))) - self.commission
                        elif data.loc[i-1, 'Holdings'] == 0:
                            data.at[i, 'Trades'] = 1000
                            data.at[i, 'Cash'] = data.loc[i-1, 'Cash'] - float((data.loc[i, 'Trades'] * price*(1+self.impact))) - self.commission
                        else:
                            data.at[i, 'Cash'] = data.loc[i-1, 'Cash']
                        # data.at[i, 'Cash'] = data.loc[i-1, 'Cash'] - float((data.loc[i, 'Trades'] * price*(1+self.impact))) - self.commission

                        data.at[i, 'Holdings'] = data.loc[i-1, 'Holdings'] + data.at[i, 'Trades'] 
                        data.at[i, 'Portfolio_Value'] = data.loc[i, 'Cash'] + price*data.loc[i, 'Holdings']
                        data.at[i, 'Daily Rets'] = data.loc[i, 'Portfolio_Value']/data.loc[i-1, 'Portfolio_Value'] - 1
                        # r = data.loc[i, 'Daily Rets']
                        # if data.loc[i-1, 'Holdings'] == 1000:
                        #     r = 0
                        
                    r = tomorrow_price/price - 1
                    
                #Short
                if action == 0:
                    price = (1-self.impact)*price
                    if i == 0:
                        data.at[i, 'Trades'] = -1000
                        data.at[i, 'Holdings'] = -1000
                        data.at[i, 'Cash'] = data.loc[i, 'Cash'] - float((-1000 * price*(1-self.impact))) - self.commission
                        data.at[i, 'Portfolio_Value'] = data.loc[i, 'Cash'] + price*data.loc[i, 'Holdings']
                        
                    else:
                        if data.loc[i-1, 'Holdings'] == 1000:
                            data.at[i, 'Trades'] = -2000
                            data.at[i, 'Cash'] = data.loc[i-1, 'Cash'] - float((data.loc[i, 'Trades'] * price*(1-self.impact))) - self.commission
                        elif data.loc[i-1, 'Holdings'] == 0:
                            data.at[i, 'Trades'] = -1000
                            data.at[i, 'Cash'] = data.loc[i-1, 'Cash'] - float((data.loc[i, 'Trades'] * price*(1-self.impact))) - self.commission
                        else:
                            data.at[i, 'Cash'] = data.loc[i-1, 'Cash']
                        # data.at[i, 'Cash'] = data.loc[i-1, 'Cash'] - float((data.loc[i, 'Trades'] * price*(1-self.impact))) - self.commission

                        data.at[i, 'Holdings'] = data.loc[i-1, 'Holdings'] + data.at[i, 'Trades'] 
                        data.at[i, 'Portfolio_Value'] = data.loc[i, 'Cash'] + price*data.loc[i, 'Holdings']
                        data.at[i, 'Daily Rets'] = data.loc[i, 'Portfolio_Value']/data.loc[i-1, 'Portfolio_Value'] - 1
                        # r = data.loc[i, 'Daily Rets']
                        # if data.loc[i-1, 'Holdings'] == -1000:
                        #     r = 0
                    
                    r = 1 - tomorrow_price/price
                action = self.learner.query(state, r)        
            
        data.set_index("index", inplace=True)	    
        df_trades = data.copy()
        df_trades.drop(columns = ["RSI", "Momentum", "Bollinger", "Daily Rets", "Portfolio_Value", "Holdings", "Cash", symbol], inplace=True)  		

        return df_trades	  	 
	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    # this uses the existing policy and test it against new data  		  	   		  	  			  		 			     			  	 
    def testPolicy(  		  	   		  	  			  		 			     			  	 
        self,  		  	   		  	  			  		 			     			  	 
        symbol="IBM",  		  	   		  	  			  		 			     			  	 
        sd=dt.datetime(2009, 1, 1),  		  	   		  	  			  		 			     			  	 
        ed=dt.datetime(2010, 1, 1),  		  	   		  	  			  		 			     			  	 
        sv=10000,  		  	   		  	  			  		 			     			  	 
    ):  		  	   		  	  			  		 			     			  	   	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
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
        
        
        
        
        i_bollinger = indicators.bollinger(prices_all)
        i_momentum = indicators.momentum(prices_all)

        i_rsi = indicators.rsi(prices_all)


        i_rsi = i_rsi.rename(columns = {symbol: "RSI"})
        i_momentum = i_momentum.rename(columns = {symbol: "Momentum"})
        i_bollinger = i_bollinger.rename(columns = {symbol: "Bollinger"})

        prices_all.dropna(inplace=True)
 
        all_2 = i_rsi.join([i_bollinger, i_momentum, prices_all])

        start = all_2.index.searchsorted(sd)


        all_2 = all_2[start:]
        
        start_rsi = i_rsi.index.searchsorted(sd) 
        start_bollinger = i_bollinger.index.searchsorted(sd) 
        start_mom = i_momentum.index.searchsorted(sd)        
        
        i_rsi = i_rsi[start_rsi:]
        i_bollinger = i_bollinger[start_bollinger:]
        i_momentum = i_momentum[start_mom:]

        all_2.reset_index(level = 0, inplace = True)	
        

        
        i_rsi = i_rsi.sort_values(by=['RSI'])
        i_bollinger = i_bollinger.sort_values(by=['Bollinger'])
        i_momentum = i_momentum.sort_values(by=['Momentum'])


        i_rsi.reset_index(level = 0, inplace = True)
        i_bollinger.reset_index(level = 0, inplace = True)
        i_momentum.reset_index(level = 0, inplace = True)


        all_2["Cash"] = 0.0
        all_2["Trades"] = 0
        all_2["Holdings"] = 0
        all_2["Portfolio_Value"] = 0.0
        all_2["Daily Rets"] = 0.0
       
        all_2.at[0, "Cash"] = float(sv)
        data = all_2.copy()
    
        first_rsi = data.loc[0, "RSI"]
        first_bb = data.loc[0, "Bollinger"]
        first_mom = data.loc[0, "Momentum"]   
        
        state = self.discretize(first_rsi, first_bb, first_mom)  # convert the location to a state  		  	   		  	  			  		 			     			  	 
        action = self.learner.querysetstate(state) 
       
        for i in data.index:		   
            rsi = data.loc[i, "RSI"]
            bb = data.loc[i, "Bollinger"]
            mom = data.loc[i, "Momentum"]
            state = self.discretize(rsi, bb, mom)
            price =  data.loc[i, symbol]
            
            
            
            #Do nothing
            if action == 2 and i == 0:
                if i == 0:
                    data.at[i, 'Portfolio_Value'] = data.loc[i, 'Cash']
                    r = data.loc[i, 'Daily Rets']
                    
                
            if i!=0 and (action == 2 or (action ==1 and data.loc[i-1, 'Holdings'] == 1000) or (action == 0 and data.loc[i-1, 'Holdings'] == -1000)):
                if i == 0:
                    data.at[i, 'Portfolio_Value'] = data.loc[i, 'Cash']

                    
                else:
                    data.at[i, 'Cash'] = data.loc[i-1, 'Cash']  
                    data.at[i, 'Trades'] = 0
                    data.at[i, 'Holdings'] = data.loc[i-1, 'Holdings']
                    data.at[i, 'Portfolio_Value'] = data.loc[i, 'Cash'] + data.loc[i, symbol]*data.loc[i, 'Holdings']
                    data.at[i, 'Daily Rets'] = data.loc[i, 'Portfolio_Value']/data.loc[i-1, 'Portfolio_Value'] - 1

            #Long
            if action == 1:
                if i == 0:
                    data.at[i, 'Trades'] = 1000
                    data.at[i, 'Holdings'] = 1000
                    data.at[i, 'Cash'] = data.loc[i, 'Cash'] - float((1000 * price*(1+self.impact))) - self.commission
                    data.at[i, 'Portfolio_Value'] = data.loc[i, 'Cash'] + price*data.loc[i, 'Holdings']

                    
                else:
                    if data.loc[i-1, 'Holdings'] == -1000:
                        data.at[i, 'Trades'] = 2000
                        data.at[i, 'Cash'] = data.loc[i-1, 'Cash'] - float((data.loc[i, 'Trades'] * price*(1+self.impact))) - self.commission
                    elif data.loc[i-1, 'Holdings'] == 0:
                        data.at[i, 'Trades'] = 1000
                        data.at[i, 'Cash'] = data.loc[i-1, 'Cash'] - float((data.loc[i, 'Trades'] * price*(1+self.impact))) - self.commission
                    else:
                        data.at[i, 'Cash'] = data.loc[i-1, 'Cash']
                    
                    # data.at[i, 'Cash'] = data.loc[i-1, 'Cash'] - float((data.loc[i, 'Trades'] * price*(1+self.impact))) - self.commission

                    data.at[i, 'Holdings'] = data.loc[i-1, 'Holdings'] + data.at[i, 'Trades'] 
                    data.at[i, 'Portfolio_Value'] = data.loc[i, 'Cash'] + price*data.loc[i, 'Holdings']
                    data.at[i, 'Daily Rets'] = data.loc[i, 'Portfolio_Value']/data.loc[i-1, 'Portfolio_Value'] - 1

                    
                
                
            #Short
            if action == 0:
                if i == 0:
                    data.at[i, 'Trades'] = -1000
                    data.at[i, 'Holdings'] = -1000
                    data.at[i, 'Cash'] = data.loc[i, 'Cash'] - float((-1000 * price*(1-self.impact))) - self.commission
                    data.at[i, 'Portfolio_Value'] = data.loc[i, 'Cash'] + price*data.loc[i, 'Holdings']

                    
                else:
                    if data.loc[i-1, 'Holdings'] == 1000:
                        data.at[i, 'Trades'] = -2000
                        data.at[i, 'Cash'] = data.loc[i-1, 'Cash'] - float((data.loc[i, 'Trades'] * price*(1-self.impact))) - self.commission
                    elif data.loc[i-1, 'Holdings'] == 0:
                        data.at[i, 'Trades'] = -1000
                        data.at[i, 'Cash'] = data.loc[i-1, 'Cash'] - float((data.loc[i, 'Trades'] * price*(1-self.impact))) - self.commission
                    else:
                        data.at[i, 'Cash'] = data.loc[i-1, 'Cash']


                    data.at[i, 'Holdings'] = data.loc[i-1, 'Holdings'] + data.at[i, 'Trades'] 
                    data.at[i, 'Portfolio_Value'] = data.loc[i, 'Cash'] + price*data.loc[i, 'Holdings']
                    data.at[i, 'Daily Rets'] = data.loc[i, 'Portfolio_Value']/data.loc[i-1, 'Portfolio_Value'] - 1

                
                
            action = self.learner.querysetstate(state)              
        # print(data)
        data.set_index("index", inplace=True)	       
        df_trades = data.copy()    
        df_trades.drop(columns = ["RSI", "Momentum", "Bollinger", "Daily Rets", "Portfolio_Value", "Holdings", "Cash", symbol], inplace=True)
  	  	   		  	  			  		 			     			  	 
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
    
    sl = StrategyLearner(impact=imp, commission=comm) 
     	   		  	  			  		 			     			  	   

    df = sl.add_evidence(symbol=sym, sd = start_in, ed=end_in, sv = 100000)  
    df = sl.testPolicy(symbol=sym, sd = start_in, ed=end_in, sv = 100000) 
    df_trades = sl.testPolicy(symbol=sym, sd = start_out, ed=end_out, sv = 100000)  

    
  	   		  	  			  		 			     			  	 
