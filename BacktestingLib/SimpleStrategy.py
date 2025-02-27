from BacktestingLib.base_strategy import BaseStrategy
from order import Order, OrderSide, OrderType

class SimpleBuyStrategy(BaseStrategy):
    def on_start(self):
        # Immediately send a market order to buy 10 shares of AAPL at start.
        order = Order(
            symbol="AAPL",
            side=OrderSide.BUY,
            quantity=20,
            order_type=OrderType.MARKET
        )
        self.send_order(order)
        print(f"SimpleBuyStrategy: Sent SELL order for 10 shares of AAPL (Order ID: {order.order_id})")

    def on_data(self, data):
        # This simple strategy does nothing on each data event.
        pass

    def on_order_execution(self, execution):
        # Print the execution receipt when the order is filled.
        print("SimpleBuyStrategy: Order executed:", execution)

    def on_end(self):
        print("SimpleBuyStrategy: Simulation ended.")
