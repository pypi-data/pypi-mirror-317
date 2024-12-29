from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime

@dataclass
class Candle:
  open_time: datetime
  close_time: datetime
  open: Decimal
  close: Decimal
  high: Decimal
  low: Decimal
  base_volume: Decimal
  quote_volume: Decimal
  trades: int
  taker_buy_base_volume: Decimal
  taker_buy_quote_volume: Decimal