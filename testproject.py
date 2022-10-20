import datetime as dt  		  	   		  	  			  		 			     			  	 
import os  		  	   		  	  			  		 			     			  	   		  	   		  	  			  		 			     			  	 
import numpy as np  		  	   		  	  			  		 			     			  	   		  	   		  	  			  		 			     			  	 
import pandas as pd  		  	   		  	  			  		 			     			  	 
from util import get_data	
import ManualStrategy 
import StrategyLearner
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
from indicators import run
import experiment1  
import experiment2


sym = "JPM"
comm = 9.95
imp = 0.005
start_in = dt.datetime(2008, 1, 1)
end_in = dt.datetime(2009, 12, 31)
start_out = dt.datetime(2010, 1, 1)
end_out = dt.datetime(2011, 12, 31)
start_val = 100000

ms = ManualStrategy.ManualStrategy(impact=imp, commission=comm, verbose = True)  	   		  	  			  		 			     			  	   

df_trades_manual_in = ms.testPolicy(symbol=sym, sd = start_in, ed=end_in, sv = start_val)  
ms.plot(df_trades_manual_in, "In-Sample Manual vs Benchmark for " + sym)

df_trades_manual_out = ms.testPolicy(symbol=sym, sd = start_out, ed=end_out, sv = start_val)  
ms.plot(df_trades_manual_out, "Out-of-Sample Manual vs Benchmark for " + sym)



sl = StrategyLearner.StrategyLearner(impact=imp, commission=comm)  	   		  	  			  		 			     			  	   

df_trades_learner_in = sl.add_evidence(symbol=sym, sd = start_in, ed=end_in, sv = start_val)  
df_trades_learner_in = sl.testPolicy(symbol=sym, sd = start_in, ed=end_in, sv = start_val) 
df_trades_learner_out = sl.testPolicy(symbol=sym, sd = start_out, ed=end_out, sv = start_val)  


experiment1.compute_data(df_trades_manual_in, df_trades_learner_in, symbol=sym, start_val=start_val, commission=comm, impact=imp, title = "In-Sample Strategy Learner vs Manual vs Benchmark")
experiment1.compute_data(df_trades_manual_out, df_trades_learner_out, symbol=sym, start_val=start_val, commission=comm, impact=imp, title = "Out-of-Sample Strategy Learner vs Manual vs Benchmark")   

experiment2.experiment2()