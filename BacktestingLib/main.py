import yfinance as yf
import pandas as pd

from BacktestingLib.Strategies.BuyAndHold import BuyAndHold
from BacktestingLib.Strategies.MovingAverageCrossover import MovingAverageCrossover
from engine import BacktestEngine

# Define universe of stocks
tickers = ['AAPL', 'NVDA', 'TSLA']

dataframe = pd.DataFrame()

# Loop over each ticker and download the 'Close' prices separately
for ticker in tickers:
    # Download only 'Close' prices for each ticker
    data = yf.download(ticker, start='2015-01-01', end='2025-01-01', auto_adjust=False)[['Close']]

    dataframe[ticker] = data

# Flatten Multi-Index Columns
dataframe.columns = [''.join(col).strip() for col in dataframe.columns]

dataframe.head()
# Instantiate the strategy
strategy = BuyAndHold(dataframe)

# Instantiate and run the backtest engine
engine = BacktestEngine(strategy, dataframe)
engine.run()

# View results
portfolio_value, trades = engine.results()