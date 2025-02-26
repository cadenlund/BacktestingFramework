from BacktestingLib.strategy import BaseStrategy

class BuyAndHold(BaseStrategy):
    def start(self):
        """Buy and Hold strategy initialization"""
        self.logs.append("Starting Buy and Hold Strategy...")

        # Calculate initial investment per ticker
        investment_per_ticker = self.cash / len(self.tickers)

        # Buy all tickers at the first date and hold
        first_date = self.data.index[0]
        for ticker in self.tickers:
            price = self.data.loc[first_date, ticker]
            shares_to_buy = investment_per_ticker / price
            self.buy(ticker, first_date, shares_to_buy)

        self.logs.append("All tickers bought at the start date. Holding until the end.")

    def calculate_signals(self, index):
        """No trading signals needed for Buy and Hold"""
        pass

    def rebalance(self, index):
        """No rebalancing for Buy and Hold"""
        pass
