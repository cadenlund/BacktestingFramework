from abc import abstractmethod
import pandas as pd

class BaseStrategy:
   def __init__(self, data, cash=100000, commission=0.001):
       #Data Assignment
       self.data = data
       self.tickers = data.columns

       #Trading parameters
       self.cash = cash
       self.initial_cash = cash
       self.commission = commission

       #Portfolio allocation
       self.positions = pd.DataFrame(0, index = self.data.index, columns=self.tickers) # array of arrays representing the holdings at each timestep
       self.weights = pd.DataFrame(0, index=self.data.index, columns=self.tickers) # array of arrays representing the weight values for each ticker at each timestep
       self.portfolio_value = pd.Series(index=self.data.index) # array of portfolio total value over time

       #logs
       self.trades = []
       self.logs = []

   def start(self, index):
       self.logs.append("Starting Backtest .......")

   def end(self, index):
       self.logs.append("Backtest Ended")
       self.evaluate()

   def next(self, index):
       #Called at each timestep
       self.calculate_signals(index)
       self.rebalance(index)

       # Update portfolio value
       self.portfolio_value[index] = (self.positions.loc[index] * self.data.loc[index]).sum() + self.cash

   def evaluate(self):
       #Calculate performance metrics
       returns = self.portfolio_value.pct_change().dropna()
       sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252)
       total_return = (self.portfolio_value.iloc[-1] - self.initial_cash) / self.initial_cash

       self.logs.append(f"Sharpe Ratio: {sharpe_ratio:.2f}")
       self.logs.append(f"Total Return: {total_return * 100:.2f}%")

   @abstractmethod
   def calculate_signals(self, index):
       #user written logic. Must be overridden
        pass

   @abstractmethod
   def rebalance(self, index):
       #User written logic. Must be overridden
        pass

   def buy(self, ticker, index, shares):
       """
       Buy shares of a stock to increase long or reduce short position.

       - If long, increases the position.
       - If short, reduces the short position (buy to cover).
       """
       price = self.data.loc[index, ticker]
       total_cost = shares * price
       commission_cost = total_cost * self.commission
       net_total = total_cost + commission_cost

       # Check if enough cash is available
       if self.cash >= net_total:
           # Increase position (long or reducing short)
           self.positions.loc[index, ticker] += shares
           self.cash -= net_total

           # Determine trade type for logging
           trade_type = 'Buy' if self.positions.loc[index, ticker] >= 0 else 'Cover'

           # Record the trade
           trade = {
               'Type': trade_type,
               'Ticker': ticker,
               'Shares': shares,
               'Price': price,
               'Total': total_cost,
               'Commission': commission_cost,
               'Net Total': net_total,
               'Cash Balance': self.cash,
               'Date': index
           }
           self.trades.append(trade)
           self.logs.append(f"{trade_type} {shares} shares of {ticker} at {price} on {index}")
       else:
           self.logs.append(f"Insufficient cash to buy {shares} shares of {ticker} on {index}")

   def sell(self, ticker, index, shares):
       """
       Sell shares of a stock to decrease long or increase short position.

       - If long, decreases the position.
       - If no position, goes short.
       - If already short, increases the short position.
       """
       price = self.data.loc[index, ticker]
       total_revenue = shares * price
       commission_cost = total_revenue * self.commission
       net_revenue = total_revenue - commission_cost

       # Decrease position (long or increasing short)
       self.positions.loc[index, ticker] -= shares
       self.cash += net_revenue

       # Determine trade type for logging
       if self.positions.loc[index, ticker] < 0:
           trade_type = 'Short'
       elif self.positions.loc[index, ticker] == 0:
           trade_type = 'Close'
       else:
           trade_type = 'Sell'

       # Record the trade
       trade = {
           'Type': trade_type,
           'Ticker': ticker,
           'Shares': shares,
           'Price': price,
           'Total': total_revenue,
           'Commission': commission_cost,
           'Net Total': net_revenue,
           'Cash Balance': self.cash,
           'Date': index
       }
       self.trades.append(trade)
       self.logs.append(f"{trade_type} {shares} shares of {ticker} at {price} on {index}")


