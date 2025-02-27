import matplotlib.pyplot as plt

class Portfolio:
    def __init__(self, starting_cash=100000.0):
        self.cash = starting_cash
        self.positions = {}      # e.g., { "AAPL": {"quantity": ..., "avg_price": ...}, ... }
        self.trade_history = []  # List of fill events.
        self.equity_history = [] # List of records: each record is a dict with keys "timestamp" and "total_value"

    def update_from_fill(self, fill):
        # Skip if invalid fill.
        if fill.get("status") != "filled" or fill.get("fill_price") is None:
            print(f"Portfolio: Skipping fill update for order {fill.get('order_id')} (status: {fill.get('status')}).")
            return

        symbol = fill['symbol']
        side = fill['side'].lower()  # expecting "buy" or "sell"
        quantity = fill['filled_quantity']
        price = fill['fill_price']

        if side == "buy":
            cost = quantity * price
            self.cash -= cost
            if symbol in self.positions:
                pos = self.positions[symbol]
                total_quantity = pos['quantity'] + quantity
                # Calculate weighted average price for the long position.
                new_avg = ((pos['quantity'] * pos['avg_price']) + (quantity * price)) / total_quantity
                self.positions[symbol] = {'quantity': total_quantity, 'avg_price': new_avg}
            else:
                self.positions[symbol] = {'quantity': quantity, 'avg_price': price}
        elif side == "sell":
            revenue = quantity * price
            self.cash += revenue
            if symbol in self.positions:
                pos = self.positions[symbol]
                # Case 1: Existing long position.
                if pos['quantity'] > 0:
                    if pos['quantity'] >= quantity:
                        new_qty = pos['quantity'] - quantity
                        if new_qty == 0:
                            del self.positions[symbol]
                        else:
                            self.positions[symbol]['quantity'] = new_qty
                    else:
                        # Sell more than long position: close long and become short for remaining.
                        remaining = quantity - pos['quantity']
                        del self.positions[symbol]
                        self.positions[symbol] = {'quantity': -remaining, 'avg_price': price}
                else:
                    # Already short: increase short position.
                    current_short_qty = -pos['quantity']  # convert to positive
                    total_short_qty = current_short_qty + quantity
                    # Update weighted average short price.
                    new_avg = ((current_short_qty * pos['avg_price']) + (quantity * price)) / total_short_qty
                    self.positions[symbol] = {'quantity': -total_short_qty, 'avg_price': new_avg}
            else:
                # No existing position: create new short position.
                self.positions[symbol] = {'quantity': -quantity, 'avg_price': price}
        else:
            raise ValueError("Invalid order side: must be 'buy' or 'sell'")

        self.trade_history.append(fill)
        print(f"Portfolio: Updated from fill. New cash: {self.cash}, positions: {self.positions}")

    def get_total_value(self, current_prices):
        """
        Calculate total portfolio value based on current cash and positions.
        current_prices: a dict mapping ticker symbols to their current market price.
        """
        total = self.cash
        for symbol, pos in self.positions.items():

            total += pos['quantity'] * current_prices['price']
        return total

    def record_equity(self, timestamp, current_prices):
        """
        Records the current total value of the portfolio.
        """
        total_value = self.get_total_value(current_prices)
        self.equity_history.append({"timestamp": timestamp, "total_value": total_value})

    def plot_equity(self):
        """
        Plots the portfolio equity (total value) over time using Matplotlib.
        """
        if not self.equity_history:
            print("No equity history to plot.")
            return

        sorted_history = sorted(self.equity_history, key=lambda x: x["timestamp"])
        timestamps = [entry["timestamp"] for entry in sorted_history]
        values = [entry["total_value"] for entry in sorted_history]

        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, values, marker='o', linestyle='-')
        plt.xlabel("Timestamp")
        plt.ylabel("Portfolio Total Value")
        plt.title("Portfolio Equity Over Time")
        plt.grid(True)
        plt.show()
