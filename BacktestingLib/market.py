import time

class BasicMarket:
    def __init__(self, portfolio):
        """
        Initialize the market simulation.
        - last_price: The most recent market price (updated via the update method).
        - fills: A list to store execution receipts (fill events).
        - portfolio: A reference to the Portfolio, used for checking available cash (for buys).
        """
        self.last_price = None
        self.fills = []
        self.portfolio = portfolio

    def update(self, event):
        if "price" in event:
            self.last_price = event["price"]

    def process_order(self, order):
        # Determine the fill price: use last known market price or order's limit price.
        fill_price = self.last_price if self.last_price is not None else order.limit_price

        if fill_price is None:
            print(f"BasicMarket: Order {order.order_id} rejected: No price available.")
            fill_receipt = {
                "order_id": order.order_id,
                "symbol": order.symbol,
                "side": order.side.value,
                "filled_quantity": 0,
                "fill_price": None,
                "status": "rejected_no_price",
                "timestamp": time.time(),
            }
            self.fills.append(fill_receipt)
            return

        # For buy orders, check for sufficient cash.
        if order.side.value == "buy":
            required_cash = order.quantity * fill_price
            if self.portfolio.cash < required_cash:
                print(f"BasicMarket: Order {order.order_id} rejected due to insufficient funds.")
                fill_receipt = {
                    "order_id": order.order_id,
                    "symbol": order.symbol,
                    "side": order.side.value,
                    "filled_quantity": 0,
                    "fill_price": None,
                    "status": "rejected_insufficient_cash",
                    "timestamp": time.time(),
                }
                self.fills.append(fill_receipt)
                return

        # For sell orders, we allow short selling, so no cash check is performed.

        # If the order passes the checks (or is a sell), execute it:
        fill_receipt = {
            "order_id": order.order_id,
            "symbol": order.symbol,
            "side": order.side.value,
            "filled_quantity": order.quantity,
            "fill_price": fill_price,
            "status": "filled",
            "timestamp": time.time(),
        }
        print(f"BasicMarket: Order {order.order_id} executed at price {fill_price}")
        self.fills.append(fill_receipt)

    def get_fills(self):
        """
        Return the list of fill receipts and clear the internal list.
        """
        fills = self.fills.copy()
        self.fills = []

        return fills