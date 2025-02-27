from enum import Enum
from dataclasses import dataclass, field
import uuid
import time

# Define the two main sides for an order
class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

# Define basic order types
class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"

@dataclass
class Order:
    symbol: str               # Asset ticker (e.g., "AAPL")
    side: OrderSide           # BUY or SELL
    quantity: float           # Number of shares/contracts to trade
    order_type: OrderType     # MARKET or LIMIT order
    limit_price: float = None # Price for limit orders; not used for market orders
    order_id: str = field(default_factory=lambda: str(uuid.uuid4()))
                              # Unique order ID generated automatically
    timestamp: float = field(default_factory=time.time)
                              # Timestamp of order creation
