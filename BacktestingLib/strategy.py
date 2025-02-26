class BaseStrategy:
   def __init__(self, data, cash=100000, commission=0.001):


       #Trading parameters
       self.data = data
       self.cash = cash
       self.initial_cash = cash
       self.commission = commission
       self