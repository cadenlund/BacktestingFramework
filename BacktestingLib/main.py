import time

from BacktestingLib.SimpleStrategy import SimpleBuyStrategy
from portfolio import Portfolio
from market import BasicMarket
from engine import Engine

if __name__ == "__main__":
    # Create a mock data feed with Apple price data.
    # Each event is a simple dict with a price and a timestamp.
    data_feed = [
        {"price": 155.0, "timestamp": time.time()},
        {"price": 156.5, "timestamp": time.time() + 2},
        {"price": 157.0, "timestamp": time.time() + 4},
        {"price": 154.0, "timestamp": time.time() + 6},
        {"price": 153.5, "timestamp": time.time() + 8},
        {"price": 155.2, "timestamp": time.time() + 10},
        {"price": 156.1, "timestamp": time.time() + 12},
        {"price": 157.8, "timestamp": time.time() + 14},
        {"price": 158.0, "timestamp": time.time() + 16},
        {"price": 157.5, "timestamp": time.time() + 18},
        {"price": 156.8, "timestamp": time.time() + 20},
        {"price": 155.9, "timestamp": time.time() + 22},
        {"price": 155.0, "timestamp": time.time() + 24},
        {"price": 154.5, "timestamp": time.time() + 26},
        {"price": 174.8, "timestamp": time.time() + 28},
        {"price": 175.4, "timestamp": time.time() + 30},
        {"price": 176.1, "timestamp": time.time() + 32},
        {"price": 177.3, "timestamp": time.time() + 34},
        {"price": 176.7, "timestamp": time.time() + 36},
        {"price": 175.6, "timestamp": time.time() + 38},
    ]

    # Initialize the portfolio with a starting cash balance.
    portfolio = Portfolio(starting_cash=100000.0)

    # Initialize the market and pass the portfolio so it can, if needed, check for cash, etc.
    market = BasicMarket(portfolio=portfolio)

    # Initialize the simple strategy that buys 10 shares of AAPL on start.
    strategy = SimpleBuyStrategy()

    # Create the Engine with a throttle interval of 1 (i.e., call strategy.on_data on every event).
    engine = Engine(market=market, strategy=strategy, data_feed=data_feed, throttle_interval=1)

    # Run the simulation.
    engine.run()

    # Print out the portfolio results and trade history.
    print("\n--- Simulation Results ---")
    print("Final Cash Balance:", portfolio.cash)
    print("Final Positions:", portfolio.positions)
    print("Trade History:")
    for trade in portfolio.trade_history:
        print(trade)

    portfolio.plot_equity()
