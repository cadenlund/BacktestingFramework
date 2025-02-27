class Engine:
    def __init__(self, market, strategy, data_feed, throttle_interval=1):
        """
        Initialize the Engine.

        :param market: An instance of a Market class.
        :param strategy: An instance of a Strategy class.
        :param data_feed: An iterable or generator that yields market events.
        :param throttle_interval: Number of events between calls to strategy.on_data.
        """
        self.market = market
        self.strategy = strategy
        self.data_feed = data_feed
        self.throttle_interval = throttle_interval
        self.event_count = 0

        if hasattr(self.strategy, 'set_engine'):
            self.strategy.set_engine(self)

    def send_order(self, order):
        """Route an order from the strategy to the market."""
        self.market.process_order(order)

    def _process_event(self, event):
        """
        Process a single event:
          - Record the portfolio's equity.
          - If throttle condition is met, call strategy.on_data and process any fills.
        """
        current_prices = self._extract_prices(event)
        timestamp = event.get("timestamp")
        self.market.portfolio.record_equity(timestamp, current_prices)

        if self.event_count % self.throttle_interval == 0:
            self.strategy.on_data(event)
            for fill in self.market.get_fills():
                self.strategy.on_order_execution(fill)
                self.market.portfolio.update_from_fill(fill)

    def run(self):
        """
        Run the simulation:
          1. Process the first event to update the market and call strategy.on_start().
          2. Then process remaining events.
          3. Finally, call strategy.on_end().
        """
        data_iter = iter(self.data_feed)
        try:
            first_event = next(data_iter)
        except StopIteration:
            self.strategy.on_start()
            self.strategy.on_end()
            return

        # Process the first event.
        self.market.update(first_event)
        self.event_count = 1
        print(f"Engine: Processed first event, last_price = {self.market.last_price}")

        # Call on_start() once now that market data is available.
        self.strategy.on_start()
        self._process_event(first_event)

        # Process remaining events.
        for event in data_iter:
            self.event_count += 1
            self.market.update(event)
            print(f"Engine: Processed event {self.event_count}, last_price = {self.market.last_price}")
            self._process_event(event)

        self.strategy.on_end()

    def _extract_prices(self, event):
        """
        Extract current prices from an event.
        Assumes event is a dict where keys (other than "timestamp") map to either:
          - A dict with a "price" key, or
          - A float representing the price.
        """
        prices = {}
        for key, value in event.items():
            if key == "timestamp":
                continue
            if isinstance(value, dict):
                prices[key] = value.get("price")
            else:
                prices[key] = value
        return prices
