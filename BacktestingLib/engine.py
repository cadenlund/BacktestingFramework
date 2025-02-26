import pandas as pd

from BacktestingLib.Strategies.MovingAverageCrossover import MovingAverageCrossover


class BacktestEngine:
    def __init__(self, strategy,  data):

        self.strategy = strategy
        self.data = data
        self.results_df = None

    def run(self):
        self.strategy.start()

        # Iterate over each time step
        for index in self.data.index:
            self.strategy.next(index)

        self.strategy.end()  # Finalize the strategy

    def results(self):
        # Collect portfolio value and trade logs
        portfolio_value = self.strategy.portfolio_value
        trades = pd.DataFrame(self.strategy.trades)

        # Display logs
        for log in self.strategy.logs:
            print(log)

        return portfolio_value, trades