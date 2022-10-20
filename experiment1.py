	  			  		 			     			  	  		  	   		  	  			  		 			     			  	 
import datetime as dt  		  	   		  	  			  		 			     			  	 
import os
from tracemalloc import start  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
import numpy as np  		  	   		  	  			  		 			     			  	 
import ManualStrategy 
import StrategyLearner  		  	   		  	  			  		 			     			  	 
import pandas as pd		  	   		  	  			  		 			     			  	 
from util import get_data, plot_data  
import matplotlib.pyplot as plt	
plt.rcParams["figure.figsize"] = (10,5)	  	   		  	  			  		 			     			  	 
  	
 		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
def compute_data(  		  	   		  	  			  		 			     			  	 
    orders_df_manual, 
    orders_df_learner, 
    symbol = 'JPM', 		  	   		  	  			  		 			     			  	 
    start_val=100000,  		  	   		  	  			  		 			     			  	 
    commission=0,  		  	   		  	  			  		 			     			  	 
    impact=0, 
    title = "In-Sample Strategy Learner vs Manual vs Benchmark"		  	   		  	  			  		 			     			  	 
):  		  	   		  	  			  		 			     			  	 

    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    orders_df = orders_df_manual.copy()  

    orders_df.index = pd.to_datetime(orders_df.index)
    orders_df_learner.index = pd.to_datetime(orders_df.index)
    
    sd = orders_df.index[0]
    ed = orders_df.index[-1]

    columns = [symbol]

    all_symbols = np.append(columns, "CASH")
    

    df1 = pd.DataFrame(index=orders_df.index, columns=all_symbols)
    df1 = df1.fillna(0.0)

    df2 = pd.DataFrame(index=orders_df.index, columns=all_symbols)
    df2 = df2.fillna(0.0)

    orders_df[symbol] = 0.0
    orders_df['Total Stock'] = 0
    orders_df['Cash'] = 0.0

    orders_df_learner[symbol] = 0.0
    orders_df_learner['Total Stock'] = 0
    orders_df_learner['Cash'] = 0.0
    
    result_learner = orders_df_learner.copy()
    result = orders_df.copy()
   
    dates = pd.date_range(sd, ed)  		  	   		  	  			  		 			     			  	 
    prices_all = get_data(columns, dates)  
    first_day = orders_df.index[0]
    
    result.at[first_day,'Cash'] = float(start_val)
    result_learner.at[first_day,'Cash'] = float(start_val)
		  	   		  	  			  		 			     			  	 


    result.reset_index(level = 0, inplace = True)
    result_learner.reset_index(level = 0, inplace = True)
    


    #Add values for holding of each stock and cash for given day
    for i in result.index:

        shares_bought = result.loc[i, 'Trades'] 
        shares_bought_learner = result_learner.loc[i, 'Trades'] 
         
        date =  result.loc[i, 'index']

        price = prices_all.loc[date, symbol] 
        
        if i == 0 and shares_bought_learner == 0:
            result_learner.at[i, 'Cash'] = float(start_val)  
            result_learner.at[i, 'Total Stock'] = shares_bought_learner
            result_learner.at[i, symbol] =  price


        if i == 0 and shares_bought_learner != 0:
            if shares_bought_learner <0:
                result_learner.at[i, 'Cash'] = float(start_val) - (float(shares_bought_learner) * price*(1-impact)) - commission  
            elif shares_bought_learner>0:
                result_learner.at[i, 'Cash'] = float(start_val) - (float(shares_bought_learner) * price*(1+impact)) - commission    
            result_learner.at[i, 'Total Stock'] = shares_bought_learner
            result_learner.at[i, symbol] =  price

        if  i>0 and shares_bought_learner == 0:
            result_learner.at[i, 'Cash'] = result_learner.loc[i-1, 'Cash']  
            result_learner.at[i, 'Total Stock'] = result_learner.loc[i-1, 'Total Stock']
            result_learner.at[i, symbol] =  price
                
        if  i>0 and shares_bought_learner !=0:
            if shares_bought_learner <0:
                result_learner.at[i, 'Cash'] = float(result_learner.loc[i-1, 'Cash']) - (float(shares_bought_learner)  * price*(1-impact)) - commission 
            elif shares_bought_learner>0:                
                result_learner.at[i, 'Cash'] = float(result_learner.loc[i-1, 'Cash']) - (float(shares_bought_learner)  * price*(1+impact)) - commission   
            result_learner.at[i, 'Total Stock'] = result_learner.loc[i-1, 'Total Stock'] + shares_bought_learner
            result_learner.at[i, symbol] =  price
                

        if i == 0 and shares_bought == 0:
            result.at[i, 'Cash'] = float(start_val)  
            result.at[i, 'Total Stock'] = shares_bought
            result.at[i, symbol] =  price


        if i == 0 and shares_bought != 0:
            if shares_bought<0:
                result.at[i, 'Cash'] = float(start_val) - (float(shares_bought) * price*(1-impact)) - commission
            elif shares_bought>0:
                result.at[i, 'Cash'] = float(start_val) - (float(shares_bought) * price*(1+impact)) - commission    
            result.at[i, 'Total Stock'] = shares_bought
            result.at[i, symbol] =  price

        if  i>0 and shares_bought == 0:
            result.at[i, 'Cash'] = result.loc[i-1, 'Cash']  
            result.at[i, 'Total Stock'] = result.loc[i-1, 'Total Stock']
            result.at[i, symbol] =  price
                
        if  i>0 and shares_bought !=0:
            if shares_bought<0:
                result.at[i, 'Cash'] = float(result.loc[i-1, 'Cash']) - (float(shares_bought)  * price*(1-impact)) - commission  
            elif shares_bought>0:
                result.at[i, 'Cash'] = float(result.loc[i-1, 'Cash']) - (float(shares_bought)  * price*(1+impact)) - commission   
            result.at[i, 'Total Stock'] = result.loc[i-1, 'Total Stock'] + shares_bought
            result.at[i, symbol] =  price            

    
    result['Portfolio_Value'] = result['Cash'] + result['Total Stock']*result[symbol] 
    result_learner['Portfolio_Value'] = result_learner['Cash'] + result_learner['Total Stock']*result_learner[symbol] 
    start_price = result.loc[0, symbol]
    bench_cash = start_val - float(start_price*1000)*(1+impact) - commission
    result['Benchmark'] = bench_cash + result[symbol]*1000  	  	   		  	  			  		 			     			  	 
	
    result.set_index('index', inplace=True)
    result_learner.set_index('index', inplace=True)

    
    optimal_df = result.copy()
    optimal_df_learner = result_learner.copy()
    
    optimal_df["Manual"] = optimal_df['Portfolio_Value']/optimal_df['Portfolio_Value'].iloc[0]
    optimal_df["Benchmark"] = optimal_df['Benchmark']/optimal_df['Benchmark'].iloc[0]
    optimal_df_learner["Strategy Learner"] = optimal_df_learner['Portfolio_Value']/optimal_df_learner['Portfolio_Value'].iloc[0]
    
    ax = optimal_df.plot(y = ["Manual", "Benchmark"], color=['r', 'purple'], title=title, grid = True)
    optimal_df_learner.plot(ax=ax, y = ["Strategy Learner"], color = 'blue', grid = True)

    
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Portfolio Return")
    plt.savefig('./images/' +title+ '.png')	

 
    
    benchmark = optimal_df['Benchmark'].copy()   
    dr_benchmark = benchmark.copy()
    dr_benchmark[1:] = (benchmark[1:] / benchmark[:-1].values) - 1   
    dr_benchmark.iloc[0] = 0
    daily_rets_benchmark = dr_benchmark[1:]
    adr_benchmark = round(daily_rets_benchmark.mean(), 6)
    sdr_benchmark = round(daily_rets_benchmark.std(), 6)
    cr_benchmark = round((benchmark[-1]/benchmark[0] - 1), 6)
    
    tos = optimal_df['Manual'].copy() 
    dr_tos = tos.copy()
    dr_tos[1:] = (tos[1:] / tos[:-1].values) - 1   
    dr_tos.iloc[0] = 0
    daily_rets_tos = dr_tos[1:]
    adr_tos = round(daily_rets_tos.mean(), 6)
    sdr_tos = round(daily_rets_tos.std(), 6)
    cr_tos = round((tos[-1]/tos[0] - 1), 6)
    
    learner = optimal_df_learner['Strategy Learner'].copy() 
    dr_learner = learner.copy()
    dr_learner[1:] = (learner[1:] / learner[:-1].values) - 1   
    dr_learner.iloc[0] = 0
    daily_rets_learner = dr_learner[1:]
    adr_learner = round(daily_rets_learner.mean(), 6)
    sdr_learner = round(daily_rets_learner.std(), 6)
    cr_learner = round((learner[-1]/learner[0] - 1), 6)
    
    print(title + ": ")  
 	   		  	  			 
    print(f"Strategy Learner Volatility (stdev of daily returns): {sdr_learner}")  		  	   		  	  			  		 			     			  	 
    print(f"Strategy Learner Average Daily Return: {adr_learner}")  		  	   		  	  			  		 			     			  	 
    print(f"Strategy Learner Cumulative Return: {cr_learner}")  
    print('\n')
     		 			     			  	 
    print(f"Manual Strategy Volatility (stdev of daily returns): {sdr_tos}")  		  	   		  	  			  		 			     			  	 
    print(f"Manual Strategy Average Daily Return: {adr_tos}")  		  	   		  	  			  		 			     			  	 
    print(f"Manual Strategy Cumulative Return: {cr_tos}")  
    print('\n')
    
    print(f"Benchmark Volatility (stdev of daily returns): {sdr_benchmark}")  		  	   		  	  			  		 			     			  	 
    print(f"Benchmark Average Daily Return: {adr_benchmark}")  		  	   		  	  			  		 			     			  	 
    print(f"Benchmark Cumulative Return: {cr_benchmark}")  
    print('\n\n')

  	   		 	
    final = result[['Portfolio_Value']].copy() 
     			  	 
    return final  		  	   		  	  			  		 			     			  	 
  		  	   	  		 			     			  	 
	  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
if __name__ == "__main__":  		  	   		  	  			  		 			     			  	 
      
    sym = "JPM"
    comm = 9.95
    imp = 0.005
    
    ms = ManualStrategy.ManualStrategy(impact=imp, commission=comm)  	   		  	  			  		 			     			  	   

    df_trades_manual_in = ms.testPolicy(symbol=sym, sd = dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)  
    ms.plot(df_trades_manual_in, "In-Sample Manual vs Benchmark for JPM")
    
    df_trades_manual_out = ms.testPolicy(symbol=sym, sd = dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv = 100000)  
    ms.plot(df_trades_manual_out, "Out-of-Sample Manual vs Benchmark for JPM")
    
    
    
    sl = StrategyLearner.StrategyLearner(impact=imp, commission=comm)  	   		  	  			  		 			     			  	   

    df_trades_learner_in = sl.add_evidence(symbol=sym, sd = dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)  
    df_trades_learner_in = sl.testPolicy(symbol=sym, sd = dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000) 
    df_trades_learner_out = sl.testPolicy(symbol=sym, sd = dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv = 100000) 	  	   		  	  			  		 			     			  	 

    compute_data(df_trades_manual_in, df_trades_learner_in, symbol=sym, start_val=100000, commission=comm, impact=imp, title = "In-Sample Strategy Learner vs Manual vs Benchmark")
    compute_data(df_trades_manual_out, df_trades_learner_out, symbol=sym, start_val=100000, commission=comm, impact=imp, title = "Out-of-Sample Strategy Learner vs Manual vs Benchmark")   
   