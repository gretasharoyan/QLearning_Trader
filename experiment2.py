import datetime as dt  		  	   		  	  			  		 			     			  	 
import os  		  	   		  	  			  		 			     			  	   		  	   		  	  			  		 			     			  	 
import numpy as np  		  	   		  	  			  		 			     			  	   		  	   		  	  			  		 			     			  	 
import pandas as pd  		  	   		  	  			  		 			     			  	 
from util import get_data, plot_data  	
import ManualStrategy 
import StrategyLearner
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10,5)
from indicators import run
import experiment1  
import math	


def plot_trades(df_portfolio, trades, title):
    
    df_portfolio[title] = df_portfolio[title] / df_portfolio[title].iloc[0] 
    ax = df_portfolio.plot(y = [title], color=['r', 'purple'], title=title, grid = True)

    for day in trades.index:

        if trades.at[day, "Trades"] > 0:
            plt.axvline(x=day, color = "blue", linestyle = "--", label = "Long" )
        if trades.at[day, "Trades"] < 0:
            plt.axvline(x=day, color = "black", linestyle = "--" , label = "Short")
    
    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio Return JPM")
    h, dc = ax.get_legend_handles_labels()
    lab = ["Manual", "Long", "Short"]
    plt.legend(handles = h, labels = lab)
    plt.savefig('./images/' +title+ '.png')	
    

def compute_stats(df, trades, title):
    
    learner = df[title].copy() 
    dr_learner = learner.copy()
    dr_learner[1:] = (learner[1:] / learner[:-1].values) - 1   
    dr_learner.iloc[0] = 0
    daily_rets_learner = dr_learner[1:]
    adr_learner = round(daily_rets_learner.mean(), 6)
    sdr_learner = round(daily_rets_learner.std(), 6)
    cr_learner = round((learner[-1]/learner[0] - 1), 6)
    sr_learner = round(math.sqrt(252.) * adr_learner / sdr_learner, 6)

    long = 0
    short = 0
    
    for day in trades.index:

        if trades.at[day, "Trades"] > 0:
            long +=1
            
        if trades.at[day, "Trades"] < 0:
            short +=1
    
    total = long + short        
    
    print(title + ": ")  
 	   		  	  			 
    print(f"Strategy Learner Volatility (stdev of daily returns): {sdr_learner}")  		  	   		  	  			  		 			     			  	 
    print(f"Strategy Learner Average Daily Return: {adr_learner}")  		  	   		  	  			  		 			     			  	 
    print(f"Strategy Learner Cumulative Return: {cr_learner}")  
    print(f"Strategy Learner Sharpe Ratio: {sr_learner}") 
    print(f"Strategy Learner Total Trade Count: {total}") 
    print('\n\n')  

def compute_val(  		  	   		  	  			  		 			     			  	 
    orders, 
    symbol = 'JPM', 		  	   		  	  			  		 			     			  	 
    sv=100000,  		  	   		  	  			  		 			     			  	 
    commission=0,  		  	   		  	  			  		 			     			  	 
    impact=0		  	   		  	  			  		 			     			  	 
):  
    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    orders_df = orders.copy()
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
    result.at[first_day,'Cash'] = float(sv)
		  	   		  	  			  		 			     			  	 


    result.reset_index(level = 0, inplace = True)

    #Add values for holding of each stock and cash for given day
    for i in result.index:

        shares_bought = result.loc[i, 'Trades']  
        date =  result.loc[i, 'index']

        price = prices_all.loc[date, symbol] 
        
        if i == 0 and shares_bought == 0:
            result.at[i, 'Cash'] = float(sv)  
            result.at[i, 'Total Stock'] = shares_bought
            result.at[i, symbol] =  price


        if i == 0 and shares_bought != 0:
            if shares_bought <0:
                result.at[i, 'Cash'] = float(sv) - (float(shares_bought) * price*(1-impact)) - commission 
            elif shares_bought>0: 
              result.at[i, 'Cash'] = float(sv) - (float(shares_bought) * price*(1+impact)) - commission    
            result.at[i, 'Total Stock'] = shares_bought
            result.at[i, symbol] =  price

        if  i>0 and shares_bought == 0:
            result.at[i, 'Cash'] = result.loc[i-1, 'Cash']  
            result.at[i, 'Total Stock'] = result.loc[i-1, 'Total Stock']
            result.at[i, symbol] =  price
                
        if  i>0 and shares_bought !=0:
            if shares_bought <0:
              result.at[i, 'Cash'] = result.at[i-1, 'Cash']  - (float(shares_bought) * price*(1-impact)) - commission 
            elif shares_bought>0: 
              result.at[i, 'Cash'] = float(result.loc[i-1, 'Cash']) - (float(shares_bought)  * price*(1+impact)) - commission   
            result.at[i, 'Total Stock'] = result.loc[i-1, 'Total Stock'] + shares_bought
            result.at[i, symbol] =  price
                

            

    
    result['Portfolio_Value'] = result['Cash'] + result['Total Stock']*result[symbol] 
    start_price = result.loc[0, symbol]
    bench_cash = sv - float(start_price*1000)*(1+impact) - commission
    result['Benchmark'] = bench_cash + result[symbol]*1000  	  	   		  	  			  		 			     			  	 
	
    result.set_index('index', inplace=True)

    
    optimal_df = result.copy()
    optimal_df["Learner"] = optimal_df['Portfolio_Value']/optimal_df['Portfolio_Value'].iloc[0]
    optimal_df["Benchmark"] = optimal_df['Benchmark']/optimal_df['Benchmark'].iloc[0]

    
    benchmark = optimal_df['Benchmark'].copy()   
    dr_benchmark = benchmark.copy()
    dr_benchmark[1:] = (benchmark[1:] / benchmark[:-1].values) - 1   
    dr_benchmark.iloc[0] = 0
    daily_rets_benchmark = dr_benchmark[1:]
    adr_benchmark = round(daily_rets_benchmark.mean(), 6)
    sdr_benchmark = round(daily_rets_benchmark.std(), 6)
    cr_benchmark = round((benchmark[-1]/benchmark[0] - 1), 6)
    
    tos = optimal_df['Learner'].copy() 
    dr_tos = tos.copy()
    dr_tos[1:] = (tos[1:] / tos[:-1].values) - 1   
    dr_tos.iloc[0] = 0
    daily_rets_tos = dr_tos[1:]
    adr_tos = round(daily_rets_tos.mean(), 6)
    sdr_tos = round(daily_rets_tos.std(), 6)
    cr_tos = round((tos[-1]/tos[0] - 1), 6)
    
  	   		 	
    final = result[['Portfolio_Value']].copy()      			  	 
    return final  		  	   		  	  	      

def experiment2():  
  
  
  
    sl1 = StrategyLearner.StrategyLearner(impact=0.00, commission=0)  	  
    sl2 = StrategyLearner.StrategyLearner(impact=0.0005, commission=0)  	
    sl3 = StrategyLearner.StrategyLearner(impact=0.005, commission=0)  	 	
    sl4 = StrategyLearner.StrategyLearner(impact=0.01, commission=0)  	
    sl5 = StrategyLearner.StrategyLearner(impact=0.05, commission=0)    	  			  		 			     			  	   

    df_trades_learner_in = sl1.add_evidence(symbol='JPM', sd = dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)  
    df_trades_learner_in_1 = sl1.testPolicy(symbol='JPM', sd = dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)  
    learner_1_val = compute_val(df_trades_learner_in_1, symbol='JPM', sv = 100000, commission=0, impact=0.00)
    learner_1_val.rename(columns={"Portfolio_Value": "Impact = 0.0",}, inplace = True)
    normal_1 = learner_1_val.copy()
    normal_1["Impact = 0.0"] = normal_1["Impact = 0.0"]/normal_1["Impact = 0.0"].iloc[0]

    df_trades_learner_in = sl2.add_evidence(symbol='JPM', sd = dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)  
    df_trades_learner_in_2 = sl2.testPolicy(symbol='JPM', sd = dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000) 
    learner_2_val = compute_val(df_trades_learner_in_2, symbol='JPM', sv = 100000, commission=9.95, impact=0.0005)
    learner_2_val.rename(columns={"Portfolio_Value": "Impact = 0.0005",}, inplace = True)
    normal_2 = learner_2_val.copy()
    normal_2["Impact = 0.0005"] = normal_2["Impact = 0.0005"]/normal_2["Impact = 0.0005"].iloc[0]
    
    df_trades_learner_in = sl3.add_evidence(symbol='JPM', sd = dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)  
    df_trades_learner_in_3 = sl3.testPolicy(symbol='JPM', sd = dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)
    learner_3_val = compute_val(df_trades_learner_in_3, symbol='JPM', sv = 100000, commission=0, impact=0.005) 
    learner_3_val.rename(columns={"Portfolio_Value": "Impact = 0.005",}, inplace = True)
    normal_3 = learner_3_val.copy()
    normal_3["Impact = 0.005"] = normal_3["Impact = 0.005"]/normal_3["Impact = 0.005"].iloc[0]
    
    df_trades_learner_in = sl4.add_evidence(symbol='JPM', sd = dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)  
    df_trades_learner_in_4 = sl4.testPolicy(symbol='JPM', sd = dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)
    learner_4_val = compute_val(df_trades_learner_in_4, symbol='JPM', sv = 100000, commission=0, impact=0.01)  
    learner_4_val.rename(columns={"Portfolio_Value": "Impact = 0.01",}, inplace = True)
    normal_4 = learner_4_val.copy()
    normal_4["Impact = 0.01"] = normal_4["Impact = 0.01"]/normal_4["Impact = 0.01"].iloc[0]
    
    df_trades_learner_in = sl5.add_evidence(symbol='JPM', sd = dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)  
    df_trades_learner_in_5 = sl5.testPolicy(symbol='JPM', sd = dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)
    learner_5_val = compute_val(df_trades_learner_in_5, symbol='JPM', sv = 100000, commission=0, impact=0.05)  
    learner_5_val.rename(columns={"Portfolio_Value": "Impact = 0.05",}, inplace = True)
    normal_5 = learner_5_val.copy()
    normal_5["Impact = 0.05"] = normal_5["Impact = 0.05"]/normal_5["Impact = 0.05"].iloc[0]
    
    all_impacts = learner_1_val.join([learner_2_val, learner_3_val, learner_4_val, learner_5_val])
    all_normal = normal_1.join([normal_2,  normal_3, normal_4, normal_5])
    
    ax = all_normal.plot(y = ["Impact = 0.0", "Impact = 0.0005", "Impact = 0.005", "Impact = 0.01", "Impact = 0.05"], color=['r', 'purple', 'green', 'orange'], title="Experiment 2: Strategy Learner w/ Varying Impacts Return for JPM", grid = True)
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Portfolio Return JPM")
    plt.savefig('./images/experiment2.png')	


    compute_stats(learner_1_val, df_trades_learner_in_1, "Impact = 0.0")
    compute_stats(learner_2_val, df_trades_learner_in_2, "Impact = 0.0005")
    compute_stats(learner_3_val, df_trades_learner_in_3, "Impact = 0.005")
    compute_stats(learner_4_val, df_trades_learner_in_4, "Impact = 0.01")
    compute_stats(learner_5_val, df_trades_learner_in_5, "Impact = 0.05")
    
    plot_trades(learner_1_val, df_trades_learner_in_1, "Impact = 0.0")
    plot_trades(learner_2_val, df_trades_learner_in_2, "Impact = 0.0005")
    plot_trades(learner_3_val, df_trades_learner_in_3, "Impact = 0.005")
    plot_trades(learner_4_val, df_trades_learner_in_4, "Impact = 0.01")
    plot_trades(learner_5_val, df_trades_learner_in_5, "Impact = 0.05")


     		 			     			  	 

if __name__ == "__main__":  		
    print("I'm in main")
    experiment2()