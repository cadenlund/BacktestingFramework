from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    def __init__(self, engine=None, params=None):
        """
        Initialize the strategy.

        :param engine: (Optional) A reference to the Engine for sending orders and accessing portfolio data.
        :param params: (Optional) A dictionary of parameters for configuring the strategy.
        """
        self.engine = engine
        self.params = params or {}

    def on_start(self):
        """
        Called once at the start of the strategy's life cycle.
        Use this to initialize variables, set up indicators, etc.
        """
        pass

    @abstractmethod
    def on_data(self, data):
        """
        Process incoming market data.

        :param data: A data structure (e.g., dict) containing market data.
                     For multi-asset support, this might be a dictionary keyed by symbol.
        """
        pass

    def on_order_execution(self, execution):
        """
        Handle updates on order execution.

        :param execution: Details of the order execution (order_id, filled quantity, price, etc.).
        """
        pass

    def send_order(self, order):
        """
        Send an order through the engine.
        The engine is responsible for routing the order to the Market.

        :param order: An order object/dictionary containing order details.
        """
        if self.engine:
            self.engine.send_order(order)
        else:
            raise NotImplementedError("Engine not set. Cannot send order.")

    def on_end(self):
        """
        Called at the end of the strategy's life cycle for cleanup or final reporting.
        """
        pass

    def set_engine(self, engine):
        """
        Allows setting the engine after initialization.

        :param engine: The engine instance to be used by the strategy.
        """
        self.engine = engine

    def get_portfolio(self):
        """
        Provides access to the portfolio values via the engine.
        This allows the strategy to read portfolio data if needed.

        :return: The portfolio instance attached to the engine, or None if not available.
        """
        if self.engine and hasattr(self.engine, 'portfolio'):
            return self.engine.portfolio
        return None
