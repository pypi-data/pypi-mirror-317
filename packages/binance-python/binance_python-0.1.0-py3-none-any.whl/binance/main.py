from dataclasses import dataclass
from binance import Spot, Public, UserStream

@dataclass
class Binance(UserStream, Public, Spot):
  ...