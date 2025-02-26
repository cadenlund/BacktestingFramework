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
       #calculate how much it is going to cost plus some fee based on the commission
       price = self.data.loc[index, ticker]
       total_cost = shares * price
       commission_cost = total_cost * self.commission
       net_total = total_cost + commission_cost

       #Next, we check if we have cash available and if we do then we add a trade record.
       if self.cash >= net_total:
           self.positions.loc[index, ticker] += shares
           self.cash -= net_total

           # Record the trade
           trade = {
               'Type': 'Buy',
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
           self.logs.append(f"Bought {shares} shares of {ticker} at {price} on {index}")
       else:
           self.logs.append(f"Insufficient cash to buy {shares} shares of {ticker} on {index}")

   def sell(self, ticker, index, shares):
       """Sell shares of a stock"""
       price = self.data.loc[index, ticker]
       total_revenue = shares * price
       commission_cost = total_revenue * self.commission
       net_revenue = total_revenue - commission_cost

       # Check if enough shares are available to sell
       if self.positions.loc[index, ticker] >= shares:
           # Update positions and cash
           self.positions.loc[index, ticker] -= shares
           self.cash += net_revenue

           # Record the trade
           trade = {
               'Type': 'Sell',
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
           self.logs.append(f"Sold {shares} shares of {ticker} at {price} on {index}")
       else:
           self.logs.append(f"Insufficient shares to sell {shares} of {ticker} on {index}")

