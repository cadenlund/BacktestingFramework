from BacktestingLib.strategy import BaseStrategy

class MovingAverageCrossover(BaseStrategy):

    def calculate_signals(self, index):
        """Calculate buy/sell signals based on Moving Average Crossover"""
        for ticker in self.tickers:
            # Calculate short-term and long-term moving averages
            short_ma = self.data[ticker].rolling(window=50).mean().loc[index]
            long_ma = self.data[ticker].rolling(window=200).mean().loc[index]

            # Generate signals
            if short_ma > long_ma:
                self.weights.loc[index, ticker] = 1  # Long position
            elif short_ma < long_ma:
                self.weights.loc[index, ticker] = 0  # Exit position
            else:
                self.weights.loc[index, ticker] = self.weights.shift(1).loc[index, ticker]  # Hold previous position

    def rebalance(self, index):
        """Rebalance the portfolio according to the calculated weights"""
        total_value = self.cash + (self.positions.loc[index] * self.data.loc[index]).sum()

        for ticker in self.tickers:
            target_value = total_value * self.weights.loc[index, ticker]
            current_value = self.positions.loc[index, ticker] * self.data.loc[index, ticker]
            order_value = target_value - current_value

            # Buy or sell shares to reach target weight
            if order_value > 0:
                shares_to_buy = order_value / self.data.loc[index, ticker]
                self.buy(ticker, index, shares_to_buy)
            elif order_value < 0:
                shares_to_sell = -order_value / self.data.loc[index, ticker]
                self.sell(ticker, index, shares_to_sell)
