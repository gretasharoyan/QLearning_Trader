The intended purpose of this README is to describe each file for the Trading Agent: Strategy Evaluation and to provide step-by-step instruction to run the code.

*********************************************************************************************************************************
Steps to Run Files Individually w/ Descriptions: "Optional Steps" can be used to create new strategy objects and change variables (dates, symbol, start value, etc). All code files already have these steps defined. To run each file individually, if there is the option, please follow the 'Mandatory Steps".  
*********************************************************************************************************************************

-----------------------------------------------------------------------------------------------------
1. testproject.py - Will run entire project. StrategyLearner.py, ManualStrategy.py, marketsimcode.py, qlearner.py, experiment1.py, experiemnt2.py, indicators.py, and marketsimcode,py are all imported in order to produce graphs for Manual Strategy, Experiment 1, and Experiment 2. Additionally, stats for Manual Strategy, Benchmark, and Strategy Learner will be generated, including Volatility, Average Daily Returns, Cumulative Return, Sharpe Ratio, and number of trades. APIs for the specific learners will be described below in their respective section. Steps to run:
 
Optional Steps:

- Symbol, commission, and impact of the all the trading strategies can be changed by reassigning the variables sym, comm, and imp, respectively

- In-sample and out-of-sample date ranges can be changed by reassigning the variables start_in and end_in (for in-sample) and start_out and end_out (for out of sample).


Mandatory Steps:

- Run line below:

PYTHONPATH=../:. python testproject.py 


-----------------------------------------------------------------------------------------------------
2. ManualStrategy.py: Will produce graphs for in-sample and out-of-sample normalized returns for the manual strategy and benchmark. Code imports marketsimcode.py  and indicators.py to produce these graphs and to calculate the Volatility, Average Daily Returns, and Cumulative Return for the manual strategy and benchmark. The manual strategy is based on Bollinger Bands, Relative Strength Index (RSI), and Momentum indicators. Steps to run:


Optional Steps:

- Symbol, commission, and impact of the all the trading strategies can be changed by reassigning the variables sym, comm, and imp, respectively

- In-sample and out-of-sample date ranges can be changed by changing the reassigning start_in and end_in (for in-sample) and start_out and end_out (for out of sample).

- A ManualStrategy object must be made using following API: manual = ManualStrategy(impact=imp, commission=comm)

- The testpolicy method must be called using following API: df_trades = manual.testPolicy(symbol='JPM', sd = start_in, ed=end_in, sv = start_val)

- the plot method must be called to plot graphs (via marketsimcode.py) using the rolling API: manual.plot(df_trades, title)


Mandatory Steps:

- Run line below: 


PYTHONPATH=../:. python ManualStrategy.py 


-----------------------------------------------------------------------------------------------------
3. StrategyLearner.py: Will create a qlearner object based on Bollinger Bands, Relative Strength Index (RSI), and Momentum indicators using in-sample data.  Learner is then tested on out-of-sample data. A trades file will be returned; however, no graphs or stats are produced in this code. Imports indicators.py to compute indicators for symbol on chosen date range and Qlearner.py to create the Q learner object. Steps to run:

Optional Steps:

- Symbol, commission, and impact of the all the trading strategies can be changed by reassigning the variables sym, comm, and imp, respectively

- In-sample and out-of-sample date ranges can be changed by reassigning the variables start_in and end_in (for in-sample) and start_out and end_out (for out of sample).

- A StrategyLearner object must be made using following API: sl = StrategyLearner(impact=0.005, commission=9.95) 

- The add_evidence method must be called to train the learner using the following API: df = sl.add_evidence(symbol=sym, sd = start_in, ed=end_in, sv = 100000) 

- The testpolicy method must be called using following API: df_trades = sl.testPolicy(symbol=sym, sd = start_out, ed=end_out, sv = 100000)


Mandatory Steps:

- Run line below: 
PYTHONPATH=../:. python StrategyLearner.py 


-----------------------------------------------------------------------------------------------------
4. experiment1.py: Will create a manual strategy object and a learner object to plots graphs and stats on both learners and the benchmark case. StrategyLearner.py and ManualStrategy.py are imported to create these objects. Please see their respective APIs in their descriptions. 


Optional Steps:

- Symbol, commission, and impact of the all the trading strategies can be changed by reassigning the variables sym, comm, and imp, respectively

- In-sample and out-of-sample date ranges can be changed by reassigning the variables start_in and end_in (for in-sample) and start_out and end_out (for out of sample).



Mandatory Steps:

- Run line below: 


PYTHONPATH=../:. python experiment1.py 

-----------------------------------------------------------------------------------------------------
5. experiment2.py: Imports StrategyLearner.py to create and train multiple learner objects with varying impact levels. Stats will be produced for all learner objects including Volatility, Average Daily Returns, Cumulative Return, Sharpe Ratio, and number of trades.  


Mandatory Steps:

- Run line below: 
PYTHONPATH=../:. python experiment2.py 


-----------------------------------------------------------------------------------------------------
6. indicators.py: Used by the various strategy objects to create policies using the defined indicators. Defined indicators include: Bollinger Bands®, Momentum, Moving Average Convergence Divergence (MACD), Relative Strength Index (RSI), and Stochastic Indicator (SI). All indicator functions accept a data frame with the adjusted closing price of a stock and return the indicator values of that stock in the form of a dataframe or series. 


-----------------------------------------------------------------------------------------------------
7. marketsimcode.py: Used by ManualStrategy.py to plot graphs and calculate stats to the Manual Strategy and the benchmark. Contains the function compute_portvals which accepts an orders data frame, symbol, starting value, impact, commission, and title (to be used on the plots) and returns the graphs and stats. 

-----------------------------------------------------------------------------------------------------
8. Qlearner.py: Used by StrategyLearner.py to create, train, and test the Q learner object.



