	  	   		  	  			  		 			     			  	 
from cProfile import label
import datetime as dt  		  	   		  	  			  		 			     			  	 
import os
from tracemalloc import start  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
import numpy as np  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
import pandas as pd  		  	   		  	  			  		 			     			  	 
from util import get_data
import matplotlib.pyplot as plt	
plt.rcParams["figure.figsize"] = (10,5)	
# import experiment1  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
def compute_portvals(  		  	   		  	  			  		 			     			  	 
    orders_df, 
    symbol = 'JPM', 		  	   		  	  			  		 			     			  	 
    start_val=100000,  		  	   		  	  			  		 			     			  	 
    commission=0,  		  	   		  	  			  		 			     			  	 
    impact=0, 
    title = "In-Sample Manual vs Benchmark", 	
    verbose = False	  	   		  	  			  		 			     			  	 
):  		  	   		  	  			  		 			     			  	 
  		  	  			  		 			     			  	 

    pd.set_option('display.float_format', lambda x: '%.2f' % x)


    orders_df.index = pd.to_datetime(orders_df.index)
    trades = orders_df.copy()   
    sd = orders_df.index[0]
    ed = orders_df.index[-1]

    columns = [symbol]

    all_symbols = np.append(columns, "CASH")

    df2 = pd.DataFrame(index=orders_df.index, columns=all_symbols)
    df2 = df2.fillna(0.0)

    orders_df[symbol] = 0.0
    orders_df['Total Stock'] = 0
    orders_df['Cash'] = 0.0

   
    result = orders_df.copy()
   
    dates = pd.date_range(sd, ed)  		  	   		  	  			  		 			     			  	 
    prices_all = get_data(columns, dates)  
    first_day = orders_df.index[0]
    result.at[first_day,'Cash'] = float(start_val)
		  	   		  	  			  		 			     			  	 


    result.reset_index(level = 0, inplace = True)

    #Add values for holding of each stock and cash for given day
    for i in result.index:

        shares_bought = result.loc[i, 'Trades']  
        date =  result.loc[i, 'index']

        price = prices_all.loc[date, symbol] 
        
        if i == 0 and shares_bought == 0:
            result.at[i, 'Cash'] = float(start_val)  
            result.at[i, 'Total Stock'] = shares_bought
            result.at[i, symbol] =  price


        if i == 0 and shares_bought != 0:
            if shares_bought <0:
                result.at[i, 'Cash'] = float(start_val) - (float(shares_bought) * price*(1-impact)) - commission  
            elif shares_bought > 0:    
                result.at[i, 'Cash'] = float(start_val) - (float(shares_bought) * price*(1+impact)) - commission    
            result.at[i, 'Total Stock'] = shares_bought
            result.at[i, symbol] =  price

        if  i>0 and shares_bought == 0:
            result.at[i, 'Cash'] = result.loc[i-1, 'Cash']  
            result.at[i, 'Total Stock'] = result.loc[i-1, 'Total Stock']
            result.at[i, symbol] =  price
                
        if  i>0 and shares_bought !=0:
            if shares_bought <0:
                result.at[i, 'Cash'] = float(result.loc[i-1, 'Cash']) - (float(shares_bought)  * price*(1-impact)) - commission   
            elif shares_bought > 0: 
                result.at[i, 'Cash'] = float(result.loc[i-1, 'Cash']) - (float(shares_bought)  * price*(1+impact)) - commission    
            result.at[i, 'Total Stock'] = result.loc[i-1, 'Total Stock'] + shares_bought
            result.at[i, symbol] =  price
                

            

    
    result['Portfolio_Value'] = result['Cash'] + result['Total Stock']*result[symbol] 
    start_price = result.loc[0, symbol]
    bench_cash = start_val - float(start_price*1000)*(1+impact) - commission
    result['Benchmark'] = bench_cash + result[symbol]*1000  
    len = result.shape[0]
 	  			  		 			     			  	 	
    result.set_index('index', inplace=True)
    
    
    optimal_df = result.copy()
    optimal_df["Manual"] = optimal_df['Portfolio_Value']/optimal_df['Portfolio_Value'].iloc[0]
    optimal_df["Benchmark"] = optimal_df['Benchmark']/optimal_df['Benchmark'].iloc[0]
    ax = optimal_df.plot(y = ["Manual", "Benchmark"], color=['r', 'purple'], title=title, grid = True)


    i1 = 0;
    i2 = 0;
    for day in trades.index:

        if trades.at[day, "Trades"] > 0:
            if i1 == 0:
                l1 = plt.axvline(x=day, color = "blue", linestyle = "--", linewidth = 2, label = "Long" )
            else:
                l1 = plt.axvline(x=day, color = "blue", linewidth = 2, linestyle = "--" )
            i1+=1
        if trades.at[day, "Trades"] < 0:
            if i2 == 0:
                l2 = plt.axvline(x=day, color = "black", linestyle = "--", linewidth = 2, label = "Short" )
            else:
                l2 = plt.axvline(x=day, color = "black", linestyle = "--" , linewidth = 2)
            i2+=1
        
    
    plt.legend() 
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
    
    if verbose:
        print(title + ": ")  
                                                                        
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
  		  	   		  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
def test_code():  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    Helper function to test code  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
	  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
if __name__ == "__main__":  		  	   		  	  			  		 			     			  	 
    test_code()  		  	   		  	  			  		 			     			  	 
