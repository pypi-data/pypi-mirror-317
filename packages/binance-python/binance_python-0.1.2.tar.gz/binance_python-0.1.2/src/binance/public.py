from typing_extensions import Literal, Generic, TypeVar, Mapping
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from .client import ClientMixin
from .types import OrderType, Error, ErrorRoot, Candle
from .util import encode_query, binance_timestamp

S = TypeVar('S', bound=str)

@dataclass
class _Base(ClientMixin):
  base: str = 'https://api.binance.com'

class PriceFilter(BaseModel):
  filterType: Literal['PRICE_FILTER']
  minPrice: str
  maxPrice: str
  tickSize: str

class LotSize(BaseModel):
  filterType: Literal['LOT_SIZE']
  minQty: str
  maxQty: str
  stepSize: str

class OtherFilter(BaseModel):
  filterType: str

Filter = PriceFilter | LotSize | OtherFilter

class SymbolInfo(BaseModel):
  symbol: str
  status: Literal['TRADING', 'BREAK', 'HALT', 'AUCTION_MATCH', 'AUCTION_OPEN', 'AUCTION_CLOSE']
  baseAsset: str
  baseAssetPrecision: int
  quoteAsset: str
  quotePrecision: int
  quoteAssetPrecision: int
  baseCommissionPrecision: int
  quoteCommissionPrecision: int
  orderTypes: list[OrderType]
  icebergAllowed: bool
  ocoAllowed: bool
  quoteOrderQtyMarketAllowed: bool
  isSpotTradingAllowed: bool
  isMarginTradingAllowed: bool
  filters: list[Filter]

  @property
  def price_filter(self) -> PriceFilter:
    for f in self.filters:
      if f.filterType == 'PRICE_FILTER':
        return f # type: ignore
    raise RuntimeError('Price filter not found')
      
  @property
  def lot_size(self) -> LotSize:
    for f in self.filters:
      if f.filterType == 'LOT_SIZE':
        return f # type: ignore
    raise RuntimeError('Lot size filter not found')

class ExchangeInfoResponse(BaseModel):
  timezone: str
  serverTime: int
  """Millis timestamp"""
  symbols: list[SymbolInfo]
  code: Literal[None] = None

@dataclass
class ExchangeInfo(Generic[S]):
  timezone: str
  serverTime: int
  """Millis timestamp"""
  symbols: Mapping[S, SymbolInfo]
  code: Literal[None] = None

@dataclass
class _ExchangeInfo(_Base):
  @ClientMixin.with_client
  async def exchange_info(self, symbol: S, *symbols: S) -> ExchangeInfo[S] | Error:
    symbols = (symbol, *symbols)
    r = await self.client.get(f'{self.base}/api/v3/exchangeInfo?symbols={encode_query(symbols)}')
    obj = r.json()
    if 'code' in obj:
      return ErrorRoot.model_validate(obj).root

    info = ExchangeInfoResponse.model_validate(obj)
    return ExchangeInfo(
      timezone=info.timezone,
      serverTime=info.serverTime,
      symbols={s.symbol: s for s in info.symbols if s.symbol in symbols}
    )

@dataclass
class Order:
  price: Decimal
  qty: Decimal

@dataclass
class OrderBook:
  lastUpdateId: int
  bids: list[Order]
  asks: list[Order]
  code: Literal[None] = None

class OrderBookResponse(BaseModel):
  lastUpdateId: int
  bids: list[tuple[str, str]]
  asks: list[tuple[str, str]]

@dataclass
class _OrderBook(_Base):
  @ClientMixin.with_client
  async def order_book(self, symbol: str, limit: int = 100) -> OrderBook | Error:
    r = await self.client.get(f'{self.base}/api/v3/depth', params={'symbol': symbol, 'limit': limit})
    obj = r.json()
    if 'code' in obj:
      return ErrorRoot.model_validate(obj).root

    data = OrderBookResponse.model_validate(obj)
    return OrderBook(
      lastUpdateId=data.lastUpdateId,
      bids=[Order(price=Decimal(p), qty=Decimal(q)) for p, q in data.bids],
      asks=[Order(price=Decimal(p), qty=Decimal(q)) for p, q in data.asks]
    )

def parse_candle(binance_array):
  return Candle(
    open_time = datetime.fromtimestamp(binance_array[0] / 1000),
    close_time = datetime.fromtimestamp(binance_array[6] / 1000),
    open = Decimal(binance_array[1]),
    close = Decimal(binance_array[4]),
    high = Decimal(binance_array[2]),
    low = Decimal(binance_array[3]),
    base_volume = Decimal(binance_array[5]),
    quote_volume = Decimal(binance_array[7]),
    trades = int(binance_array[8]),
    taker_buy_base_volume = Decimal(binance_array[9]),
    taker_buy_quote_volume = Decimal(binance_array[10])
  )

@dataclass
class _Candles(_Base):
  @ClientMixin.with_client
  async def candles(
    self, pair: str, start: datetime | None = None, *,
    interval: str, limit: int = 1000,
  ) -> list[Candle]:
    params  = {'symbol': pair, 'interval': interval, 'limit': limit}
    if start is not None:
      params['startTime'] = binance_timestamp(start)
    endpoint = self.base + '/api/v3/klines'
    r = await self.client.get(endpoint, params=params)
    return list(map(parse_candle, r.json()))


@dataclass
class Public(_ExchangeInfo, _OrderBook, _Candles):
  base: str = 'https://api.binance.com'

  @ClientMixin.with_client
  async def price(self, symbol: str) -> Decimal:
    r = await self.client.get(f'{self.base}/api/v3/ticker/price', params={'symbol': symbol})
    return Decimal(r.json()['price'])
  